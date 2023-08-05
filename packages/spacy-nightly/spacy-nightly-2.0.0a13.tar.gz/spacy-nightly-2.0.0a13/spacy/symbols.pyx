# coding: utf8
from __future__ import unicode_literals

IDS = {
    "": NIL,
    "IS_ALPHA": IS_ALPHA,
    "IS_ASCII": IS_ASCII,
    "IS_DIGIT": IS_DIGIT,
    "IS_LOWER": IS_LOWER,
    "IS_PUNCT": IS_PUNCT,
    "IS_SPACE": IS_SPACE,
    "IS_TITLE": IS_TITLE,
    "IS_UPPER": IS_UPPER,
    "LIKE_URL": LIKE_URL,
    "LIKE_NUM": LIKE_NUM,
    "LIKE_EMAIL": LIKE_EMAIL,
    "IS_STOP": IS_STOP,
    "IS_OOV": IS_OOV,
    "FLAG14": FLAG14,
    "FLAG15": FLAG15,
    "FLAG16": FLAG16,
    "FLAG17": FLAG17,
    "FLAG18": FLAG18,
    "FLAG19": FLAG19,
    "FLAG20": FLAG20,
    "FLAG21": FLAG21,
    "FLAG22": FLAG22,
    "FLAG23": FLAG23,
    "FLAG24": FLAG24,
    "FLAG25": FLAG25,
    "FLAG26": FLAG26,
    "FLAG27": FLAG27,
    "FLAG28": FLAG28,
    "FLAG29": FLAG29,
    "FLAG30": FLAG30,
    "FLAG31": FLAG31,
    "FLAG32": FLAG32,
    "FLAG33": FLAG33,
    "FLAG34": FLAG34,
    "FLAG35": FLAG35,
    "FLAG36": FLAG36,
    "FLAG37": FLAG37,
    "FLAG38": FLAG38,
    "FLAG39": FLAG39,
    "FLAG40": FLAG40,
    "FLAG41": FLAG41,
    "FLAG42": FLAG42,
    "FLAG43": FLAG43,
    "FLAG44": FLAG44,
    "FLAG45": FLAG45,
    "FLAG46": FLAG46,
    "FLAG47": FLAG47,
    "FLAG48": FLAG48,
    "FLAG49": FLAG49,
    "FLAG50": FLAG50,
    "FLAG51": FLAG51,
    "FLAG52": FLAG52,
    "FLAG53": FLAG53,
    "FLAG54": FLAG54,
    "FLAG55": FLAG55,
    "FLAG56": FLAG56,
    "FLAG57": FLAG57,
    "FLAG58": FLAG58,
    "FLAG59": FLAG59,
    "FLAG60": FLAG60,
    "FLAG61": FLAG61,
    "FLAG62": FLAG62,
    "FLAG63": FLAG63,

    "ID": ID,
    "ORTH": ORTH,
    "LOWER": LOWER,
    "NORM": NORM,
    "SHAPE": SHAPE,
    "PREFIX": PREFIX,
    "SUFFIX": SUFFIX,

    "LENGTH": LENGTH,
    "CLUSTER": CLUSTER,
    "LEMMA": LEMMA,
    "POS": POS,
    "TAG": TAG,
    "DEP": DEP,
    "ENT_IOB": ENT_IOB,
    "ENT_TYPE": ENT_TYPE,
    "HEAD": HEAD,
    "SENT_START": SENT_START,
    "SPACY": SPACY,
    "PROB": PROB,

    "ADJ": ADJ,
    "ADP": ADP,
    "ADV": ADV,
    "AUX": AUX,
    "CONJ": CONJ,
    "CCONJ": CCONJ, # U20
    "DET": DET,
    "INTJ": INTJ,
    "NOUN": NOUN,
    "NUM": NUM,
    "PART": PART,
    "PRON": PRON,
    "PROPN": PROPN,
    "PUNCT": PUNCT,
    "SCONJ": SCONJ,
    "SYM": SYM,
    "VERB": VERB,
    "X": X,
    "EOL": EOL,
    "SPACE": SPACE,

    "Animacy_anim": Animacy_anim,
    "Animacy_inam": Animacy_inam,
    "Animacy_hum": Animacy_hum, # U20
    "Aspect_freq": Aspect_freq,
    "Aspect_imp": Aspect_imp,
    "Aspect_mod": Aspect_mod,
    "Aspect_none": Aspect_none,
    "Aspect_perf": Aspect_perf,
    "Aspect_iter": Aspect_iter, # U20
    "Aspect_hab": Aspect_hab, # U20
    "Case_abe": Case_abe,
    "Case_abl": Case_abl,
    "Case_abs": Case_abs,
    "Case_acc": Case_acc,
    "Case_ade": Case_ade,
    "Case_all": Case_all,
    "Case_cau": Case_cau,
    "Case_com": Case_com,
    "Case_cmp": Case_cmp, # U20
    "Case_dat": Case_dat,
    "Case_del": Case_del,
    "Case_dis": Case_dis,
    "Case_ela": Case_ela,
    "Case_equ": Case_equ, # U20
    "Case_ess": Case_ess,
    "Case_gen": Case_gen,
    "Case_ill": Case_ill,
    "Case_ine": Case_ine,
    "Case_ins": Case_ins,
    "Case_loc": Case_loc,
    "Case_lat": Case_lat,
    "Case_nom": Case_nom,
    "Case_par": Case_par,
    "Case_sub": Case_sub,
    "Case_sup": Case_sup,
    "Case_tem": Case_tem,
    "Case_ter": Case_ter,
    "Case_tra": Case_tra,
    "Case_voc": Case_voc,
    "Definite_two": Definite_two,
    "Definite_def": Definite_def,
    "Definite_red": Definite_red,
    "Definite_cons": Definite_cons, # U20
    "Definite_ind": Definite_ind,
    "Definite_spec": Definite_spec, # U20
    "Degree_cmp": Degree_cmp,
    "Degree_comp": Degree_comp,
    "Degree_none": Degree_none,
    "Degree_pos": Degree_pos,
    "Degree_sup": Degree_sup,
    "Degree_abs": Degree_abs,
    "Degree_com": Degree_com,
    "Degree_dim ": Degree_dim, # du
    "Degree_equ": Degree_equ, # U20
    "Evident_nfh": Evident_nfh, # U20
    "Gender_com": Gender_com,
    "Gender_fem": Gender_fem,
    "Gender_masc": Gender_masc,
    "Gender_neut": Gender_neut,
    "Mood_cnd": Mood_cnd,
    "Mood_imp": Mood_imp,
    "Mood_ind": Mood_ind,
    "Mood_n": Mood_n,
    "Mood_pot": Mood_pot,
    "Mood_sub": Mood_sub,
    "Mood_opt": Mood_opt,
    "Mood_prp": Mood_prp, # U20
    "Mood_adm": Mood_adm, # U20
    "Negative_neg": Negative_neg,
    "Negative_pos": Negative_pos,
    "Negative_yes": Negative_yes,
    "Polarity_neg": Polarity_neg, # U20
    "Polarity_pos": Polarity_pos, # U20
    "Number_com": Number_com,
    "Number_dual": Number_dual,
    "Number_none": Number_none,
    "Number_plur": Number_plur,
    "Number_sing": Number_sing,
    "Number_ptan ": Number_ptan, # bg
    "Number_count ": Number_count, # bg, U20
    "Number_tri": Number_tri, # U20
    "NumType_card": NumType_card,
    "NumType_dist": NumType_dist,
    "NumType_frac": NumType_frac,
    "NumType_gen": NumType_gen,
    "NumType_mult": NumType_mult,
    "NumType_none": NumType_none,
    "NumType_ord": NumType_ord,
    "NumType_sets": NumType_sets,
    "Person_one": Person_one,
    "Person_two": Person_two,
    "Person_three": Person_three,
    "Person_none": Person_none,
    "Poss_yes": Poss_yes,
    "PronType_advPart": PronType_advPart,
    "PronType_art": PronType_art,
    "PronType_default": PronType_default,
    "PronType_dem": PronType_dem,
    "PronType_ind": PronType_ind,
    "PronType_int": PronType_int,
    "PronType_neg": PronType_neg,
    "PronType_prs": PronType_prs,
    "PronType_rcp": PronType_rcp,
    "PronType_rel": PronType_rel,
    "PronType_tot": PronType_tot,
    "PronType_clit": PronType_clit,
    "PronType_exc": PronType_exc, # es, ca, it, fa, U20
    "PronType_emp": PronType_emp, # U20
    "Reflex_yes": Reflex_yes,
    "Tense_fut": Tense_fut,
    "Tense_imp": Tense_imp,
    "Tense_past": Tense_past,
    "Tense_pres": Tense_pres,
    "VerbForm_fin": VerbForm_fin,
    "VerbForm_ger": VerbForm_ger,
    "VerbForm_inf": VerbForm_inf,
    "VerbForm_none": VerbForm_none,
    "VerbForm_part": VerbForm_part,
    "VerbForm_partFut": VerbForm_partFut,
    "VerbForm_partPast": VerbForm_partPast,
    "VerbForm_partPres": VerbForm_partPres,
    "VerbForm_sup": VerbForm_sup,
    "VerbForm_trans": VerbForm_trans,
    "VerbForm_conv": VerbForm_conv, # U20
    "VerbForm_gdv ": VerbForm_gdv, # la,
    "VerbForm_vnoun": VerbForm_vnoun, # U20
    "Voice_act": Voice_act,
    "Voice_cau": Voice_cau,
    "Voice_pass": Voice_pass,
    "Voice_mid ": Voice_mid, # gkc, U20
    "Voice_int ": Voice_int, # hb,
    "Voice_antip": Voice_antip, # U20
    "Voice_dir": Voice_dir, # U20
    "Voice_inv": Voice_inv, # U20
    "Abbr_yes ": Abbr_yes, # cz, fi, sl, U,
    "AdpType_prep ": AdpType_prep, # cz, U,
    "AdpType_post ": AdpType_post, # U,
    "AdpType_voc ": AdpType_voc, # cz,
    "AdpType_comprep ": AdpType_comprep, # cz,
    "AdpType_circ ": AdpType_circ, # U,
    "AdvType_man": AdvType_man,
    "AdvType_loc": AdvType_loc,
    "AdvType_tim": AdvType_tim,
    "AdvType_deg": AdvType_deg,
    "AdvType_cau": AdvType_cau,
    "AdvType_mod": AdvType_mod,
    "AdvType_sta": AdvType_sta,
    "AdvType_ex": AdvType_ex,
    "AdvType_adadj": AdvType_adadj,
    "ConjType_oper ": ConjType_oper, # cz, U,
    "ConjType_comp ": ConjType_comp, # cz, U,
    "Connegative_yes ": Connegative_yes, # fi,
    "Derivation_minen ": Derivation_minen, # fi,
    "Derivation_sti ": Derivation_sti, # fi,
    "Derivation_inen ": Derivation_inen, # fi,
    "Derivation_lainen ": Derivation_lainen, # fi,
    "Derivation_ja ": Derivation_ja, # fi,
    "Derivation_ton ": Derivation_ton, # fi,
    "Derivation_vs ": Derivation_vs, # fi,
    "Derivation_ttain ": Derivation_ttain, # fi,
    "Derivation_ttaa ": Derivation_ttaa, # fi,
    "Echo_rdp ": Echo_rdp, # U,
    "Echo_ech ": Echo_ech, # U,
    "Foreign_foreign ": Foreign_foreign, # cz, fi, U,
    "Foreign_fscript ": Foreign_fscript, # cz, fi, U,
    "Foreign_tscript ": Foreign_tscript, # cz, U,
    "Foreign_yes ": Foreign_yes, # sl,
    "Gender_dat_masc ": Gender_dat_masc, # bq, U,
    "Gender_dat_fem ": Gender_dat_fem, # bq, U,
    "Gender_erg_masc ": Gender_erg_masc, # bq,
    "Gender_erg_fem ": Gender_erg_fem, # bq,
    "Gender_psor_masc ": Gender_psor_masc, # cz, sl, U,
    "Gender_psor_fem ": Gender_psor_fem, # cz, sl, U,
    "Gender_psor_neut ": Gender_psor_neut, # sl,
    "Hyph_yes ": Hyph_yes, # cz, U,
    "InfForm_one ": InfForm_one, # fi,
    "InfForm_two ": InfForm_two, # fi,
    "InfForm_three ": InfForm_three, # fi,
    "NameType_geo ": NameType_geo, # U, cz,
    "NameType_prs ": NameType_prs, # U, cz,
    "NameType_giv ": NameType_giv, # U, cz,
    "NameType_sur ": NameType_sur, # U, cz,
    "NameType_nat ": NameType_nat, # U, cz,
    "NameType_com ": NameType_com, # U, cz,
    "NameType_pro ": NameType_pro, # U, cz,
    "NameType_oth ": NameType_oth, # U, cz,
    "NounType_com ": NounType_com, # U,
    "NounType_prop ": NounType_prop, # U,
    "NounType_class ": NounType_class, # U,
    "Number_abs_sing ": Number_abs_sing, # bq, U,
    "Number_abs_plur ": Number_abs_plur, # bq, U,
    "Number_dat_sing ": Number_dat_sing, # bq, U,
    "Number_dat_plur ": Number_dat_plur, # bq, U,
    "Number_erg_sing ": Number_erg_sing, # bq, U,
    "Number_erg_plur ": Number_erg_plur, # bq, U,
    "Number_psee_sing ": Number_psee_sing, # U,
    "Number_psee_plur ": Number_psee_plur, # U,
    "Number_psor_sing ": Number_psor_sing, # cz, fi, sl, U,
    "Number_psor_plur ": Number_psor_plur, # cz, fi, sl, U,
    "Number_pauc": Number_pauc, # U20
    "Number_grpa": Number_grpa, # U20
    "Number_grpl": Number_grpl, # U20
    "Number_inv": Number_inv, # U20
    "NumForm_digit": NumForm_digit, # cz, sl, U,
    "NumForm_roman": NumForm_roman, # cz, sl, U,
    "NumForm_word": NumForm_word, # cz, sl, U,
    "NumValue_one": NumValue_one, # cz, U,
    "NumValue_two": NumValue_two, # cz, U,
    "NumValue_three": NumValue_three, # cz, U,
    "PartForm_pres": PartForm_pres, # fi,
    "PartForm_past": PartForm_past, # fi,
    "PartForm_agt": PartForm_agt, # fi,
    "PartForm_neg": PartForm_neg, # fi,
    "PartType_mod": PartType_mod, # U,
    "PartType_emp": PartType_emp, # U,
    "PartType_res": PartType_res, # U,
    "PartType_inf": PartType_inf, # U,
    "PartType_vbp": PartType_vbp, # U,
    "Person_abs_one": Person_abs_one, # bq, U,
    "Person_abs_two": Person_abs_two, # bq, U,
    "Person_abs_three": Person_abs_three, # bq, U,
    "Person_dat_one": Person_dat_one, # bq, U,
    "Person_dat_two": Person_dat_two, # bq, U,
    "Person_dat_three": Person_dat_three, # bq, U,
    "Person_erg_one": Person_erg_one, # bq, U,
    "Person_erg_two": Person_erg_two, # bq, U,
    "Person_erg_three": Person_erg_three, # bq, U,
    "Person_psor_one": Person_psor_one, # fi, U,
    "Person_psor_two": Person_psor_two, # fi, U,
    "Person_psor_three": Person_psor_three, # fi, U,
    "Person_zero": Person_zero, # U20
    "Person_four": Person_four, # U20
    "Polite_inf": Polite_inf, # bq, U,
    "Polite_pol": Polite_pol, # bq, U,
    "Polite_abs_inf": Polite_abs_inf, # bq, U,
    "Polite_abs_pol": Polite_abs_pol, # bq, U,
    "Polite_erg_inf": Polite_erg_inf, # bq, U,
    "Polite_erg_pol": Polite_erg_pol, # bq, U,
    "Polite_dat_inf": Polite_dat_inf, # bq, U,
    "Polite_dat_pol": Polite_dat_pol, # bq, U,
    "Polite_infm": Polite_infm, # U20
    "Polite_form": Polite_form, # U20
    "Polite_form_elev": Polite_form_elev, # U20
    "Polite_form_humb ": Polite_form_humb, # U20
    "Prefix_yes": Prefix_yes, # U,
    "PrepCase_npr": PrepCase_npr, # cz,
    "PrepCase_pre": PrepCase_pre, # U,
    "PunctSide_ini": PunctSide_ini, # U,
    "PunctSide_fin": PunctSide_fin, # U,
    "PunctType_peri": PunctType_peri, # U,
    "PunctType_qest": PunctType_qest, # U,
    "PunctType_excl": PunctType_excl, # U,
    "PunctType_quot": PunctType_quot, # U,
    "PunctType_brck": PunctType_brck, # U,
    "PunctType_comm": PunctType_comm, # U,
    "PunctType_colo": PunctType_colo, # U,
    "PunctType_semi": PunctType_semi, # U,
    "PunctType_dash": PunctType_dash, # U,
    "Style_arch": Style_arch, # cz, fi, U,
    "Style_rare": Style_rare, # cz, fi, U,
    "Style_poet": Style_poet, # cz, U,
    "Style_norm": Style_norm, # cz, U,
    "Style_coll": Style_coll, # cz, U,
    "Style_vrnc": Style_vrnc, # cz, U,
    "Style_sing": Style_sing, # cz, U,
    "Style_expr": Style_expr, # cz, U,
    "Style_derg": Style_derg, # cz, U,
    "Style_vulg": Style_vulg, # cz, U,
    "Style_yes": Style_yes, # fi, U,
    "StyleVariant_styleShort": StyleVariant_styleShort, # cz,
    "StyleVariant_styleBound": StyleVariant_styleBound, # cz, sl,
    "VerbType_aux": VerbType_aux, # U,
    "VerbType_cop": VerbType_cop, # U,
    "VerbType_mod": VerbType_mod, # U,
    "VerbType_light": VerbType_light, # U,

    "PERSON": PERSON,
    "NORP": NORP,
    "FACILITY": FACILITY,
    "ORG": ORG,
    "GPE": GPE,
    "LOC": LOC,
    "PRODUCT": PRODUCT,
    "EVENT": EVENT,
    "WORK_OF_ART": WORK_OF_ART,
    "LANGUAGE": LANGUAGE,

    "DATE": DATE,
    "TIME": TIME,
    "PERCENT": PERCENT,
    "MONEY": MONEY,
    "QUANTITY": QUANTITY,
    "ORDINAL": ORDINAL,
    "CARDINAL": CARDINAL,

    "acomp": acomp,
    "advcl": advcl,
    "advmod": advmod,
    "agent": agent,
    "amod": amod,
    "appos": appos,
    "attr": attr,
    "aux": aux,
    "auxpass": auxpass,
    "cc": cc,
    "ccomp": ccomp,
    "complm": complm,
    "conj": conj,
    "cop": cop, # U20
    "csubj": csubj,
    "csubjpass": csubjpass,
    "dep": dep,
    "det": det,
    "dobj": dobj,
    "expl": expl,
    "hmod": hmod,
    "hyph": hyph,
    "infmod": infmod,
    "intj": intj,
    "iobj": iobj,
    "mark": mark,
    "meta": meta,
    "neg": neg,
    "nmod": nmod,
    "nn": nn,
    "npadvmod": npadvmod,
    "nsubj": nsubj,
    "nsubjpass": nsubjpass,
    "num": num,
    "number": number,
    "oprd": oprd,
    "obj": obj, # U20
    "obl": obl, # U20
    "parataxis": parataxis,
    "partmod": partmod,
    "pcomp": pcomp,
    "pobj": pobj,
    "poss": poss,
    "possessive": possessive,
    "preconj": preconj,
    "prep": prep,
    "prt": prt,
    "punct": punct,
    "quantmod": quantmod,
    "rcmod": rcmod,
    "root": root,
    "xcomp": xcomp
}

NAMES = [it[0] for it in sorted(IDS.items(), key=lambda it: it[1])]
