# coding: utf8
from __future__ import unicode_literals
from collections import defaultdict

cimport numpy as np
import numpy
import numpy.linalg
from libc.math cimport sqrt

from .doc cimport token_by_start, token_by_end, get_token_attr
from ..structs cimport TokenC, LexemeC
from ..typedefs cimport flags_t, attr_t, hash_t
from ..attrs cimport attr_id_t
from ..parts_of_speech cimport univ_pos_t
from ..util import normalize_slice
from ..attrs cimport IS_PUNCT, IS_SPACE
from ..lexeme cimport Lexeme
from ..compat import is_config
from .. import about


cdef class Span:
    """A slice from a Doc object."""
    def __cinit__(self, Doc doc, int start, int end, attr_t label=0, vector=None,
                  vector_norm=None):
        """Create a `Span` object from the slice `doc[start : end]`.

        doc (Doc): The parent document.
        start (int): The index of the first token of the span.
        end (int): The index of the first token after the span.
        label (uint64): A label to attach to the Span, e.g. for named entities.
        vector (ndarray[ndim=1, dtype='float32']): A meaning representation of the span.
        RETURNS (Span): The newly constructed object.
        """
        if not (0 <= start <= end <= len(doc)):
            raise IndexError

        self.doc = doc
        self.start = start
        self.start_char = self.doc[start].idx if start < self.doc.length else 0
        self.end = end
        if end >= 1:
            self.end_char = self.doc[end - 1].idx + len(self.doc[end - 1])
        else:
            self.end_char = 0
        assert label in doc.vocab.strings, label
        self.label = label
        self._vector = vector
        self._vector_norm = vector_norm

    def __richcmp__(self, Span other, int op):
        # Eq
        if op == 0:
            return self.start_char < other.start_char
        elif op == 1:
            return self.start_char <= other.start_char
        elif op == 2:
            return self.start_char == other.start_char and self.end_char == other.end_char
        elif op == 3:
            return self.start_char != other.start_char or self.end_char != other.end_char
        elif op == 4:
            return self.start_char > other.start_char
        elif op == 5:
            return self.start_char >= other.start_char

    def __hash__(self):
        return hash((self.doc, self.label, self.start_char, self.end_char))

    def __len__(self):
        """Get the number of tokens in the span.

        RETURNS (int): The number of tokens in the span.
        """
        self._recalculate_indices()
        if self.end < self.start:
            return 0
        return self.end - self.start

    def __repr__(self):
        if is_config(python3=True):
            return self.text
        return self.text.encode('utf-8')

    def __getitem__(self, object i):
        """Get a `Token` or a `Span` object

        i (int or tuple): The index of the token within the span, or slice of
            the span to get.
        RETURNS (Token or Span): The token at `span[i]`.

        EXAMPLE:
            >>> span[0]
            >>> span[1:3]
        """
        self._recalculate_indices()
        if isinstance(i, slice):
            start, end = normalize_slice(len(self), i.start, i.stop, i.step)
            return Span(self.doc, start + self.start, end + self.start)
        else:
            if i < 0:
                return self.doc[self.end + i]
            else:
                return self.doc[self.start + i]

    def __iter__(self):
        """Iterate over `Token` objects.

        YIELDS (Token): A `Token` object.
        """
        self._recalculate_indices()
        for i in range(self.start, self.end):
            yield self.doc[i]

    def merge(self, *args, **attributes):
        """Retokenize the document, such that the span is merged into a single
        token.

        **attributes: Attributes to assign to the merged token. By default,
            attributes are inherited from the syntactic root token of the span.
        RETURNS (Token): The newly merged token.
        """
        return self.doc.merge(self.start_char, self.end_char, *args, **attributes)

    def similarity(self, other):
        """Make a semantic similarity estimate. The default estimate is cosine
        similarity using an average of word vectors.

        other (object): The object to compare with. By default, accepts `Doc`,
            `Span`, `Token` and `Lexeme` objects.
        RETURNS (float): A scalar similarity score. Higher is more similar.
        """
        if 'similarity' in self.doc.user_span_hooks:
            self.doc.user_span_hooks['similarity'](self, other)
        if self.vector_norm == 0.0 or other.vector_norm == 0.0:
            return 0.0
        return numpy.dot(self.vector, other.vector) / (self.vector_norm * other.vector_norm)

    cpdef np.ndarray to_array(self, object py_attr_ids):
        """Given a list of M attribute IDs, export the tokens to a numpy
        `ndarray` of shape `(N, M)`, where `N` is the length of the document.
        The values will be 32-bit integers.

        attr_ids (list[int]): A list of attribute ID ints.
        RETURNS (numpy.ndarray[long, ndim=2]): A feature matrix, with one row
            per word, and one column per attribute indicated in the input
            `attr_ids`.
        """
        cdef int i, j
        cdef attr_id_t feature
        cdef np.ndarray[attr_t, ndim=2] output
        # Make an array from the attributes --- otherwise our inner loop is Python
        # dict iteration.
        cdef np.ndarray[attr_t, ndim=1] attr_ids = numpy.asarray(py_attr_ids, dtype=numpy.uint64)
        cdef int length = self.end - self.start
        output = numpy.ndarray(shape=(length, len(attr_ids)), dtype=numpy.uint64)
        for i in range(self.start, self.end):
            for j, feature in enumerate(attr_ids):
                output[i-self.start, j] = get_token_attr(&self.doc.c[i], feature)
        return output

    cpdef int _recalculate_indices(self) except -1:
        if self.end > self.doc.length \
        or self.doc.c[self.start].idx != self.start_char \
        or (self.doc.c[self.end-1].idx + self.doc.c[self.end-1].lex.length) != self.end_char:
            start = token_by_start(self.doc.c, self.doc.length, self.start_char)
            if self.start == -1:
                raise IndexError("Error calculating span: Can't find start")
            end = token_by_end(self.doc.c, self.doc.length, self.end_char)
            if end == -1:
                raise IndexError("Error calculating span: Can't find end")

            self.start = start
            self.end = end + 1

    property sent:
        """The sentence span that this span is a part of.

        RETURNS (Span): The sentence span that the span is a part of.
        """
        def __get__(self):
            if 'sent' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['sent'](self)
            # This should raise if we're not parsed.
            self.doc.sents
            cdef int n = 0
            root = &self.doc.c[self.start]
            while root.head != 0:
                root += root.head
                n += 1
                if n >= self.doc.length:
                    raise RuntimeError
            return self.doc[root.l_edge : root.r_edge + 1]

    property has_vector:
        """A boolean value indicating whether a word vector is associated with
        the object.

        RETURNS (bool): Whether a word vector is associated with the object.
        """
        def __get__(self):
            if 'has_vector' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['has_vector'](self)
            return any(token.has_vector for token in self)

    property vector:
        """A real-valued meaning representation. Defaults to an average of the
        token vectors.

        RETURNS (numpy.ndarray[ndim=1, dtype='float32']): A 1D numpy array
            representing the span's semantics.
        """
        def __get__(self):
            if 'vector' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['vector'](self)
            if self._vector is None:
                self._vector = sum(t.vector for t in self) / len(self)
            return self._vector

    property vector_norm:
        """The L2 norm of the document's vector representation.

        RETURNS (float): The L2 norm of the vector representation.
        """
        def __get__(self):
            if 'vector_norm' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['vector'](self)
            cdef float value
            cdef double norm = 0
            if self._vector_norm is None:
                norm = 0
                for value in self.vector:
                    norm += value * value
                self._vector_norm = sqrt(norm) if norm != 0 else 0
            return self._vector_norm

    property sentiment:
        # TODO: docstring
        def __get__(self):
            if 'sentiment' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['sentiment'](self)
            else:
                return sum([token.sentiment for token in self]) / len(self)

    property text:
        """A unicode representation of the span text.

        RETURNS (unicode): The original verbatim text of the span.
        """
        def __get__(self):
            text = self.text_with_ws
            if self[-1].whitespace_:
                text = text[:-1]
            return text

    property text_with_ws:
        """The text content of the span with a trailing whitespace character if
        the last token has one.

        RETURNS (unicode): The text content of the span (with trailing whitespace).
        """
        def __get__(self):
            return u''.join([t.text_with_ws for t in self])

    property noun_chunks:
        """Yields base noun-phrase `Span` objects, if the document has been
        syntactically parsed. A base noun phrase, or "NP chunk", is a noun
        phrase that does not permit other NPs to be nested within it – so no
        NP-level coordination, no prepositional phrases, and no relative clauses.

        YIELDS (Span): Base noun-phrase `Span` objects
        """
        def __get__(self):
            if not self.doc.is_parsed:
                raise ValueError(
                    "noun_chunks requires the dependency parse, which "
                    "requires data to be installed. For more info, see the "
                    "documentation: \n%s\n" % about.__docs_models__)
            # Accumulate the result before beginning to iterate over it. This prevents
            # the tokenisation from being changed out from under us during the iteration.
            # The tricky thing here is that Span accepts its tokenisation changing,
            # so it's okay once we have the Span objects. See Issue #375
            spans = []
            cdef attr_t label
            for start, end, label in self.doc.noun_chunks_iterator(self):
                spans.append(Span(self, start, end, label=label))
            for span in spans:
                yield span

    property root:
        """The token within the span that's highest in the parse tree.
        If there's a tie, the earliest is prefered.

        RETURNS (Token): The root token.

        EXAMPLE: The root token has the shortest path to the root of the sentence
            (or is the root itself). If multiple words are equally high in the
            tree, the first word is taken. For example:

            >>> toks = nlp(u'I like New York in Autumn.')

            Let's name the indices – easier than writing `toks[4]` etc.

            >>> i, like, new, york, in_, autumn, dot = range(len(toks))

            The head of 'new' is 'York', and the head of "York" is "like"

            >>> toks[new].head.text
            'York'
            >>> toks[york].head.text
            'like'

            Create a span for "New York". Its root is "York".

            >>> new_york = toks[new:york+1]
            >>> new_york.root.text
            'York'

            Here's a more complicated case, raised by issue #214:

            >>> toks = nlp(u'to, north and south carolina')
            >>> to, north, and_, south, carolina = toks
            >>> south.head.text, carolina.head.text
            ('north', 'to')

            Here "south" is a child of "north", which is a child of "carolina".
            Carolina is the root of the span:

            >>> south_carolina = toks[-2:]
            >>> south_carolina.root.text
            'carolina'
        """
        def __get__(self):
            self._recalculate_indices()
            if 'root' in self.doc.user_span_hooks:
                return self.doc.user_span_hooks['root'](self)
            # This should probably be called 'head', and the other one called
            # 'gov'. But we went with 'head' elsehwhere, and now we're stuck =/
            cdef int i
            # First, we scan through the Span, and check whether there's a word
            # with head==0, i.e. a sentence root. If so, we can return it. The
            # longer the span, the more likely it contains a sentence root, and
            # in this case we return in linear time.
            for i in range(self.start, self.end):
                if self.doc.c[i].head == 0:
                    return self.doc[i]
            # If we don't have a sentence root, we do something that's not so
            # algorithmically clever, but I think should be quite fast, especially
            # for short spans.
            # For each word, we count the path length, and arg min this measure.
            # We could use better tree logic to save steps here...But I think this
            # should be okay.
            cdef int current_best = self.doc.length
            cdef int root = -1
            for i in range(self.start, self.end):
                if self.start <= (i+self.doc.c[i].head) < self.end:
                    continue
                words_to_root = _count_words_to_root(&self.doc.c[i], self.doc.length)
                if words_to_root < current_best:
                    current_best = words_to_root
                    root = i
            if root == -1:
                return self.doc[self.start]
            else:
                return self.doc[root]

    property lefts:
        """ Tokens that are to the left of the span, whose head is within the
        `Span`.

        YIELDS (Token):A left-child of a token of the span.
        """
        def __get__(self):
            for token in reversed(self): # Reverse, so we get the tokens in order
                for left in token.lefts:
                    if left.i < self.start:
                        yield left

    property rights:
        """Tokens that are to the right of the Span, whose head is within the
        `Span`.

        YIELDS (Token): A right-child of a token of the span.
        """
        def __get__(self):
            for token in self:
                for right in token.rights:
                    if right.i >= self.end:
                        yield right

    property subtree:
        """Tokens that descend from tokens in the span, but fall outside it.

        YIELDS (Token): A descendant of a token within the span.
        """
        def __get__(self):
            for word in self.lefts:
                yield from word.subtree
            yield from self
            for word in self.rights:
                yield from word.subtree

    property ent_id:
        """An (integer) entity ID. Usually assigned by patterns in the `Matcher`.

        RETURNS (uint64): The entity ID.
        """
        def __get__(self):
            return self.root.ent_id

        def __set__(self, hash_t key):
            # TODO
            raise NotImplementedError(
                "Can't yet set ent_id from Span. Vote for this feature on the issue "
                "tracker: http://github.com/explosion/spaCy/issues")

    property ent_id_:
        """A (string) entity ID. Usually assigned by patterns in the `Matcher`.

        RETURNS (unicode): The entity ID.
        """
        def __get__(self):
            return self.root.ent_id_

        def __set__(self, hash_t key):
            # TODO
            raise NotImplementedError(
                "Can't yet set ent_id_ from Span. Vote for this feature on the issue "
                "tracker: http://github.com/explosion/spaCy/issues")

    property orth_:
        # TODO: docstring
        def __get__(self):
            return ''.join([t.string for t in self]).strip()

    property lemma_:
        """The span's lemma.

        RETURNS (unicode): The span's lemma.
        """
        def __get__(self):
            return ' '.join([t.lemma_ for t in self]).strip()

    property upper_:
        # TODO: docstring
        def __get__(self):
            return ''.join([t.string.upper() for t in self]).strip()

    property lower_:
        # TODO: docstring
        def __get__(self):
            return ''.join([t.string.lower() for t in self]).strip()

    property string:
        # TODO: docstring
        def __get__(self):
            return ''.join([t.string for t in self])

    property label_:
        """The span's label.

        RETURNS (unicode): The span's label.
        """
        def __get__(self):
            return self.doc.vocab.strings[self.label]


cdef int _count_words_to_root(const TokenC* token, int sent_length) except -1:
    # Don't allow spaces to be the root, if there are
    # better candidates
    if Lexeme.c_check_flag(token.lex, IS_SPACE) and token.l_kids == 0 and token.r_kids == 0:
        return sent_length-1
    if Lexeme.c_check_flag(token.lex, IS_PUNCT) and token.l_kids == 0 and token.r_kids == 0:
        return sent_length-1
    cdef int n = 0
    while token.head != 0:
        token += token.head
        n += 1
        if n >= sent_length:
            raise RuntimeError(
                "Array bounds exceeded while searching for root word. This likely "
                "means the parse tree is in an invalid state. Please report this "
                "issue here: http://github.com/explosion/spaCy/issues")
    return n
