# Decision tree structure
# Leaf nodes are strings (final results)
# Branch nodes have "question", "yes", and "no" keys

decision_tree_1 = {

    # -------------------------
    # 1.1
    # -------------------------
    "q_1_1": {
        "question": "1.1. Is it possible for the impact of the exposure or the effectiveness of the intervention to be confounded in this study?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no"],
        "mapping": {
            "yes": "q_1_2",
            "seemingly yes": "q_1_2",
            "seemingly no": "result_low_risk_a",
            "no": "result_low_risk_a"
        }
    },

    # -------------------------
    # 1.2
    # -------------------------
    "q_1_2": {
        "question": "1.2. Did the author(s) control for all the potential confounders?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_1_4_a",
            "seemingly yes": "q_1_4_a",
            "no": "q_1_3",
            "seemingly no": "q_1_3",
            "unclear": "q_1_3"
        }
    },

    # -------------------------
    # 1.3
    # -------------------------
    "q_1_3": {
        "question": "1.3. Is there any justifiable reason for not controlling for all the potential confounders?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no"],
        "mapping": {
            "yes": "q_1_4_b",
            "seemingly yes": "q_1_4_b",
            "no": "result_high_risk_d",
            "seemingly no": "result_high_risk_d"
        }
    },

    # -------------------------
    # 1.4 (Path A: from 1.2 YES)
    # -------------------------
    "q_1_4_a": {
        "question": "1.4. Were the potential confounders measured accurately and precisely enough?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_1_5_a",
            "seemingly yes": "q_1_5_a",
            "no": "q_1_5_a",
            "seemingly no": "q_1_5_a",
            "unclear": "q_1_5_a"
        }
    },

    # -------------------------
    # 1.5 (Path A)
    # -------------------------
    "q_1_5_a": {
        "question": "1.5. Did the author(s) analyse the effect appropriately taking confounders into account?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_low_risk_b",
            "seemingly yes": "result_low_risk_b",
            "no": "result_medium_risk_c",
            "seemingly no": "result_medium_risk_c",
            "unclear": "result_medium_risk_c"
        }
    },

    # -------------------------
    # 1.4 (Path B: from 1.3 YES)
    # -------------------------
    "q_1_4_b": {
        "question": "1.4. Were the potential confounders measured accurately and precisely enough?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_1_5_b",
            "seemingly yes": "q_1_5_b",
            "no": "q_1_5_b",
            "seemingly no": "q_1_5_b",
            "unclear": "q_1_5_b"
        }
    },

    # -------------------------
    # 1.5 (Path B)
    # -------------------------
    "q_1_5_b": {
        "question": "1.5. Did the author(s) analyse the effect appropriately taking confounders into account?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_low_risk_b",
            "seemingly yes": "result_low_risk_b",
            "no": "result_high_risk_d",
            "seemingly no": "result_high_risk_d",
            "unclear": "result_high_risk_d"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low_risk_a": "LOW RISK: Confounding is not considered possible.",
    "result_low_risk_b": "LOW RISK: Confounders appropriately handled.",
    "result_medium_risk_c": "MEDIUM RISK: Analysis of confounders was not appropriate.",
    "result_high_risk_d": "HIGH RISK: Confounding not properly addressed."
}

decision_tree_2 = {
    # -------------------------
    # 2.1
    # -------------------------
    "q_2_1": {
        "question": "2.1.a. Was the selection of subjects or areas after intervention or exposure random or systematic... OR 2.1.b. Was the entire (or nearly entire) population of inference followed-up after intervention or exposure, and exchangeability between before and after groups could be assumed?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_2_a",
            "seemingly yes": "q_2_2_a",
            "seemingly no": "q_2_2_b",
            "no": "q_2_2_b",
            "unclear": "q_2_2_b"
        }
    },

    # -------------------------
    # 2.2 (Path A: from 2.1 YES/SY)
    # -------------------------
    "q_2_2_a": {
        "question": "2.2. Was/were the researcher(s) unaware (or blinded) of the selection of subjects or areas?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_3_a",
            "seemingly yes": "q_2_3_a",
            "seemingly no": "q_2_3_a",
            "no": "q_2_3_a",
            "unclear": "q_2_3_a"
        }
    },

    # -------------------------
    # 2.3 (Path A: Left side)
    # -------------------------
    "q_2_3_a": {
        "question": "2.3. After the start of the intervention/exposure or during the analysis, were any subjects or areas excluded or lost from the study or analysis?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_4",
            "seemingly yes": "q_2_4",
            "seemingly no": "result_low",
            "no": "result_low",
            "unclear": "q_2_4"
        }
    },

    # -------------------------
    # 2.2 (Path B: from 2.1 NO/SN/Unclear)
    # -------------------------
    "q_2_2_b": {
        "question": "2.2. Was/were the researcher(s) unaware (or blinded) of the selection of subjects or areas?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_3_b",
            "seemingly yes": "q_2_3_b",
            "seemingly no": "q_2_3_b",
            "no": "q_2_3_b",
            "unclear": "q_2_3_b"
        }
    },

    # -------------------------
    # 2.3 (Path B: Right side)
    # -------------------------
    "q_2_3_b": {
        "question": "2.3. After the start of the intervention/exposure or during the analysis, were any subjects or areas excluded or lost from the study or analysis?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_4",
            "seemingly yes": "q_2_4",
            "seemingly no": "q_2_4",
            "no": "q_2_4",
            "unclear": "q_2_4"
        }
    },

    # -------------------------
    # 2.4
    # -------------------------
    "q_2_4": {
        "question": "2.4. Were the subjects or areas included in the study (or analysis) comparable between groups and so they allowed a valid comparison to be made (i.e., exchangeability or conditional exchangeability between groups could be assumed)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "seemingly no": "q_2_5",
            "no": "q_2_5",
            "unclear": "q_2_5"
        }
    },

    # -------------------------
    # 2.5
    # -------------------------
    "q_2_5": {
        "question": "2.5. Were the difference(s) between groups likely to be explained by the intervention/exposure or a variable influenced by the intervention/exposure (including the outcome)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_2_6",
            "seemingly yes": "q_2_6",
            "seemingly no": "result_med",
            "no": "result_med",
            "unclear": "q_2_6"
        }
    },

    # -------------------------
    # 2.6
    # -------------------------
    "q_2_6": {
        "question": "2.6. Did the author(s) adjust for the potential post-intervention/exposure selection bias in an appropriate way?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "seemingly no": "result_high",
            "no": "result_high",
            "unclear": "result_high"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low": "LOW RISK",
    "result_med": "MEDIUM RISK",
    "result_high": "HIGH RISK"
}

decision_tree_3 = {
    # -------------------------
    # INITIAL ROUTING
    # -------------------------
    "start": {
        "question": "Is this an experimental study (i.e., interventions or exposures are formally applied to evaluate effects) rather than an observational study (i.e., comparisons of groups of interest without formal application of interventions or exposures)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_not_applicable",
            "seemingly yes": "result_not_applicable",
            "seemingly no": "q_3_1",
            "no": "q_3_1",
            "unclear": "q_3_1"
        }
    },

    # -------------------------
    # 3.1
    # -------------------------
    "q_3_1": {
        "question": "3.1. Were the intervention or exposure (group) and the comparator (group) of interest sufficiently well-defined so that no meaningful vagueness remains for the intended assessment of causal effect of interest?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_3_2_a",
            "seemingly yes": "q_3_2_a",
            "seemingly no": "q_3_2_b",
            "no": "q_3_2_b",
            "unclear": "q_3_2_b"
        }
    },

    # -------------------------
    # 3.2 (Path A: from 3.1 YES)
    # -------------------------
    "q_3_2_a": {
        "question": "3.2. Were the observed intervention or exposure (group) and the comparator (group) appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_3_3_a",
            "seemingly yes": "q_3_3_a",
            "seemingly no": "q_3_3_b",
            "no": "q_3_3_b",
            "unclear": "q_3_3_b"
        }
    },

    # -------------------------
    # 3.2 (Path B: from 3.1 NO)
    # -------------------------
    "q_3_2_b": {
        "question": "3.2. Were the observed intervention or exposure (group) and the comparator (group) appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_3_3_b",
            "seemingly yes": "q_3_3_b",
            "seemingly no": "q_3_3_c",
            "no": "q_3_3_c",
            "unclear": "q_3_3_c"
        }
    },

    # -------------------------
    # 3.3 (Path A: from 3.2_a YES)
    # -------------------------
    "q_3_3_a": {
        "question": "3.3. Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_medium_risk",
            "seemingly yes": "result_medium_risk",
            "seemingly no": "result_low_risk",
            "no": "result_low_risk",
            "unclear": "result_medium_risk"
        }
    },

    # -------------------------
    # 3.3 (Path B: from 3.2_a NO or 3.2_b YES)
    # -------------------------
    "q_3_3_b": {
        "question": "3.3. Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_high_risk",
            "seemingly yes": "result_high_risk",
            "seemingly no": "result_medium_risk",
            "no": "result_medium_risk",
            "unclear": "result_high_risk"
        }
    },

    # -------------------------
    # 3.3 (Path C: from 3.2_b NO)
    # -------------------------
    "q_3_3_c": {
        "question": "3.3. Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_high_risk",
            "seemingly yes": "result_high_risk",
            "seemingly no": "result_medium_risk",
            "no": "result_medium_risk",
            "unclear": "result_high_risk"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK",
    "result_not_applicable": "NOT APPLICABLE: This tree is only for observational studies."
}

decision_tree_4 = {

    # -------------------------
    # INITIAL ROUTING
    # -------------------------
    "start": {
        "question": "Is this an experimental study (i.e., interventions or exposures are formally applied to evaluate effects) rather than an observational study (i.e., comparisons of groups of interest without formal application of interventions or exposures)?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_1",
            "seemingly yes": "q_4_1",
            "seemingly no": "result_not_applicable",
            "no": "result_not_applicable",
            "unclear": "q_4_1"
        }
    },

    # -------------------------
    # 4.1
    # -------------------------
    "q_4_1": {
        "question": "4.1. Were any of the persons, who applied or received treatments (intervention, exposure, alternative intervention, alternative exposure, or control), aware of the hypothesis that was being tested or the comparison that was being made?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_2",
            "seemingly yes": "q_4_2",
            "no": "q_4_2",
            "seemingly no": "q_4_2",
            "unclear": "q_4_2"
        }
    },

    # -------------------------
    # 4.2
    # -------------------------
    "q_4_2": {
        "question": "4.2. Were there any alterations of intervention/exposure or control treatments of interest that might have an impact on the effectiveness of the intervention or the impact of the exposure?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_3",
            "seemingly yes": "q_4_3",
            "unclear": "q_4_3",
            "no": "q_4_4_a",
            "seemingly no": "q_4_4_a"
        }
    },

    # -------------------------
    # 4.3
    # -------------------------
    "q_4_3": {
        "question": "4.3. Were these deviated treatments unbalanced between intervention or exposure groups (when comparing two interventions or exposures), or inaccurately taken into account (when comparing intervention or exposure vs. control, and thus it might have influenced the estimate of impact or effectiveness?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_4_c",
            "seemingly yes": "q_4_4_c",
            "unclear": "q_4_4_c",
            "no": "q_4_4_b",
            "seemingly no": "q_4_4_b"
        }
    },

    # -------------------------
    # 4.4 (Path A: Left branch, from 4.2 NO)
    # -------------------------
    "q_4_4_a": {
        "question": "4.4. Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_low",
            "seemingly yes": "result_low",
            "no": "q_4_5_a",
            "seemingly no": "q_4_5_a",
            "unclear": "q_4_5_a"
        }
    },

    # -------------------------
    # 4.4 (Path B: Center branch, from 4.3 NO)
    # -------------------------
    "q_4_4_b": {
        "question": "4.4. Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_5_a",
            "seemingly yes": "q_4_5_a",
            "no": "q_4_5_b",
            "seemingly no": "q_4_5_b",
            "unclear": "q_4_5_b"
        }
    },

    # -------------------------
    # 4.4 (Path C: Right branch, from 4.3 YES)
    # -------------------------
    "q_4_4_c": {
        "question": "4.4. Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "q_4_5_b",
            "seemingly yes": "q_4_5_b",
            "no": "q_4_5_b",
            "seemingly no": "q_4_5_b",
            "unclear": "q_4_5_b"
        }
    },

    # -------------------------
    # 4.5 (Path A: Center branch)
    # -------------------------
    "q_4_5_a": {
        "question": "4.5. Are the used analysis methods of the impact of the exposure or the effectiveness of the intervention appropriate in relation to bias due to altered treatment procedure of interest?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "no": "result_high",
            "seemingly no": "result_high",
            "unclear": "result_high"
        }
    },

    # -------------------------
    # 4.5 (Path B: Right branch)
    # -------------------------
    "q_4_5_b": {
        "question": "4.5. Are the used analysis methods of the impact of the exposure or the effectiveness of the intervention appropriate in relation to bias due to altered treatment procedure of interest?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "no": "result_high",
            "seemingly no": "result_high",
            "unclear": "result_high"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low": "LOW",
    "result_med": "MED",
    "result_high": "HIGH",
    "result_not_applicable": "NOT APPLICABLE: This tree is only for experimental studies."
}


decision_tree_5 = {

    # -------------------------
    # 5.1
    # -------------------------
    "q_5_1": {
        "question": "5.1. Was there any way for the outcome measure to be affected by knowledge of the exposure, intervention, subjects or areas, or desire for certain outcome? (E.g., select Y/SY if data collectors who measured the outcome or human subjects who report their outcomes were aware of the details of the study.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_5_2_b",
            "seemingly yes": "q_5_2_b",
            "unclear (yes)": "q_5_2_b",
            "seemingly no": "q_5_2_a",
            "no": "q_5_2_a"
        }
    },

    # -------------------------
    # 5.2 (Path A: from 5.1 No/SN - Left side of diagram)
    # -------------------------
    "q_5_2_a": {
        "question": "5.2. Was the measured outcome appropriate for the intended assessment of causal effect (i.e., causal effect of interest)? (E.g., select Y/SY if the measured outcome is consistent with the intended outcome; select N/SN if measured outcome is different from the pre-specified outcome or inappropriate for the intended assessment of causal effect.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (no)"],
        "mapping": {
            "yes": "q_5_3_a",
            "seemingly yes": "q_5_3_a",
            "seemingly no": "q_5_3_b",
            "no": "q_5_3_b",
            "unclear (no)": "q_5_3_b"
        }
    },

    # -------------------------
    # 5.2 (Path B: from 5.1 Yes/SY - Right side of diagram)
    # -------------------------
    "q_5_2_b": {
        "question": "5.2. Was the measured outcome appropriate for the intended assessment of causal effect (i.e., causal effect of interest)? (E.g., select Y/SY if the measured outcome is consistent with the intended outcome; select N/SN if measured outcome is different from the pre-specified outcome or inappropriate for the intended assessment of causal effect.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (no)"],
        "mapping": {
            "yes": "q_5_3_b",
            "seemingly yes": "q_5_3_b",
            "seemingly no": "q_5_3_b",
            "no": "q_5_3_b",
            "unclear (no)": "q_5_3_b"
        }
    },

    # -------------------------
    # 5.3 (Path A: Left side of diagram)
    # -------------------------
    "q_5_3_a": {
        "question": "5.3. Were the methods for measuring the outcome data the same across the groups? (E.g., select N/SN if the outcome was measured at different time windows between groups (e.g., 2 weeks after intervention vs. 4 weeks after control treatment). When exactly the same methods cannot be used among the groups due to the nature of the study, assessors may select Y/SY if the methods are sufficiently comparable. E.g., if a study measure bird species diversity in fields, and detectability of species is slightly different between groups but the slight difference in detectability can be considered comparable.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (no)"],
        "mapping": {
            "yes": "result_low",
            "seemingly yes": "result_low",
            "seemingly no": "q_5_4",
            "no": "q_5_4",
            "unclear (no)": "q_5_4"
        }
    },

    # -------------------------
    # 5.3 (Path B: Right side of diagram)
    # -------------------------
    "q_5_3_b": {
        "question": "5.3. Were the methods for measuring the outcome data the same across the groups? (E.g., select N/SN if the outcome was measured at different time windows between groups (e.g., 2 weeks after intervention vs. 4 weeks after control treatment). When exactly the same methods cannot be used among the groups due to the nature of the study, assessors may select Y/SY if the methods are sufficiently comparable. E.g., if a study measure bird species diversity in fields, and detectability of species is slightly different between groups but the slight difference in detectability can be considered comparable.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (no)"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "seemingly no": "q_5_4",
            "no": "q_5_4",
            "unclear (no)": "q_5_4"
        }
    },

    # -------------------------
    # 5.4 
    # -------------------------
    "q_5_4": {
        "question": "5.4. Were the potential differences in measured outcomes between groups investigated and adjusted/corrected if necessary? (Differences in measured outcomes between groups can be a source of detection bias.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (no)"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "seemingly no": "result_high",
            "no": "result_high",
            "unclear (no)": "result_high"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low": "LOW RISK",
    "result_med": "MEDIUM RISK",
    "result_high": "HIGH RISK"
}

decision_tree_6 = {

    # -------------------------
    # 6.1
    # -------------------------
    "q_6_1": {
        "question": "6.1. Are the reported relevant outcome data (or effect estimate) likely to be of (or based on) selected measurements of the outcome? (I.e., only a part of measured outcomes is reported. E.g., only 80 measured outcomes are reported when there are 100, or the effect estimate is based on 80 measured outcomes when there are 100.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_6_2_right",
            "seemingly yes": "q_6_2_right",
            "unclear (yes)": "q_6_2_right",
            "seemingly no": "q_6_2_left",
            "no": "q_6_2_left"
        }
    },

    # -------------------------
    # 6.2 (Left Path: from 6.1 NO)
    # -------------------------
    "q_6_2_left": {
        "question": "6.2. Are relevant outcome data likely to be unreported for some subgroup(s)? (I.e., only outcome data on certain subjects or areas with certain characteristic(s) (e.g., taxonomic group) or in certain conditions (e.g., intervention intensity) are available.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_6_3_middle",
            "seemingly yes": "q_6_3_middle",
            "unclear (yes)": "q_6_3_middle",
            "seemingly no": "q_6_3_left",
            "no": "q_6_3_left"
        }
    },

    # -------------------------
    # 6.2 (Right Path: from 6.1 YES)
    # -------------------------
    "q_6_2_right": {
        "question": "6.2. Are relevant outcome data likely to be unreported for some subgroup(s)? (I.e., only outcome data on certain subjects or areas with certain characteristic(s) (e.g., taxonomic group) or in certain conditions (e.g., intervention intensity) are available.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_6_3_right",
            "seemingly yes": "q_6_3_right",
            "unclear (yes)": "q_6_3_right",
            "seemingly no": "q_6_3_middle",
            "no": "q_6_3_middle"
        }
    },

    # -------------------------
    # 6.3 (Left Path: from 6.2 Left NO)
    # -------------------------
    "q_6_3_left": {
        "question": "6.3. Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported? (I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "unclear (yes)": "result_med",
            "seemingly no": "result_low",
            "no": "result_low"
        }
    },

    # -------------------------
    # 6.3 (Middle Path: from 6.2 Left YES or 6.2 Right NO)
    # -------------------------
    "q_6_3_middle": {
        "question": "6.3. Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported? (I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_high",
            "seemingly yes": "result_high",
            "unclear (yes)": "result_high",
            "seemingly no": "result_med",
            "no": "result_med"
        }
    },

    # -------------------------
    # 6.3 (Right Path: from 6.2 Right YES)
    # -------------------------
    "q_6_3_right": {
        "question": "6.3. Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported? (I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_high",
            "seemingly yes": "result_high",
            "unclear (yes)": "result_high",
            "seemingly no": "result_high",
            "no": "result_high"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low": "LOW",
    "result_med": "MED",
    "result_high": "HIGH"
}

decision_tree_7 = {

    # -------------------------
    # INITIAL ROUTING
    # -------------------------
    "start": {
        "question": "Were inferential statistics conducted in this study?",
        "valid_answers": ["yes", "no"],
        "mapping": {
            "yes": "q_7_1_inf",
            "no": "q_7_1_no_inf"
        }
    },

    # ==========================================================
    # PATH A: INFERENTIAL STATISTICS NOT CONDUCTED (LEFT TREE)
    # ==========================================================

    # -------------------------
    # 7.1 (No Inferential Stats)
    # -------------------------
    "q_7_1_no_inf": {
        "question": "7.1. Was/were the person(s), who estimated the effectiveness of the intervention or the impact of the exposure, aware of the exposure or intervention received by subjects or areas? (E.g., select Y/SY if analysts were aware of the details of the study.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_2_no_inf_b",
            "seemingly yes": "q_7_2_no_inf_b",
            "unclear (yes)": "q_7_2_no_inf_b",
            "no": "q_7_2_no_inf_a",
            "seemingly no": "q_7_2_no_inf_a"
        }
    },

    # -------------------------
    # 7.2 (No Inferential Stats - Left Branch)
    # -------------------------
    "q_7_2_no_inf_a": {
        "question": "7.2. Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses? (E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "unclear (yes)": "result_med",
            "no": "result_low",
            "seemingly no": "result_low"
        }
    },

    # -------------------------
    # 7.2 (No Inferential Stats - Right Branch)
    # -------------------------
    "q_7_2_no_inf_b": {
        "question": "7.2. Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses? (E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_high",
            "seemingly yes": "result_high",
            "unclear (yes)": "result_high",
            "no": "result_med",
            "seemingly no": "result_med"
        }
    },

    # ==========================================================
    # PATH B: INFERENTIAL STATISTICS CONDUCTED (RIGHT TREE)
    # ==========================================================
    # Note: L = Left column, M = Middle column, R = Right column
    # ==========================================================

    # -------------------------
    # 7.1 (Inferential Stats)
    # -------------------------
    "q_7_1_inf": {
        "question": "7.1. Was/were the person(s), who estimated the effectiveness of the intervention or the impact of the exposure, aware of the exposure or intervention received by subjects or areas? (E.g., select Y/SY if analysts were aware of the details of the study.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_2_inf_m",
            "seemingly yes": "q_7_2_inf_m",
            "unclear (yes)": "q_7_2_inf_m",
            "no": "q_7_2_inf_l",
            "seemingly no": "q_7_2_inf_l"
        }
    },

    # -------------------------
    # 7.2 (Inferential Stats - Left Column)
    # -------------------------
    "q_7_2_inf_l": {
        "question": "7.2. Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses? (E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_3_inf_m",
            "seemingly yes": "q_7_3_inf_m",
            "unclear (yes)": "q_7_3_inf_m",
            "no": "q_7_3_inf_l",
            "seemingly no": "q_7_3_inf_l"
        }
    },

    # -------------------------
    # 7.2 (Inferential Stats - Middle Column)
    # -------------------------
    "q_7_2_inf_m": {
        "question": "7.2. Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses? (E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_3_inf_r",
            "seemingly yes": "q_7_3_inf_r",
            "unclear (yes)": "q_7_3_inf_r",
            "no": "q_7_3_inf_m",
            "seemingly no": "q_7_3_inf_m"
        }
    },

    # -------------------------
    # 7.3 (Inferential Stats - Left Column)
    # -------------------------
    "q_7_3_inf_l": {
        "question": "7.3. Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)? (E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_4_inf_m",
            "seemingly yes": "q_7_4_inf_m",
            "unclear (yes)": "q_7_4_inf_m",
            "no": "q_7_4_inf_l",
            "seemingly no": "q_7_4_inf_l"
        }
    },

    # -------------------------
    # 7.3 (Inferential Stats - Middle Column)
    # -------------------------
    "q_7_3_inf_m": {
        "question": "7.3. Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)? (E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_4_inf_r",
            "seemingly yes": "q_7_4_inf_r",
            "unclear (yes)": "q_7_4_inf_r",
            "no": "q_7_4_inf_m",
            "seemingly no": "q_7_4_inf_m"
        }
    },

    # -------------------------
    # 7.3 (Inferential Stats - Right Column)
    # -------------------------
    "q_7_3_inf_r": {
        "question": "7.3. Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)? (E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "q_7_4_inf_r",
            "seemingly yes": "q_7_4_inf_r",
            "unclear (yes)": "q_7_4_inf_r",
            "no": "q_7_4_inf_r",
            "seemingly no": "q_7_4_inf_r"
        }
    },

    # -------------------------
    # 7.4 (Inferential Stats - Left Column)
    # -------------------------
    "q_7_4_inf_l": {
        "question": "7.4. Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)? (E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test...)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_med",
            "seemingly yes": "result_med",
            "unclear (yes)": "result_med",
            "no": "result_low",
            "seemingly no": "result_low"
        }
    },

    # -------------------------
    # 7.4 (Inferential Stats - Middle Column)
    # -------------------------
    "q_7_4_inf_m": {
        "question": "7.4. Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)? (E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test...)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_high",
            "seemingly yes": "result_high",
            "unclear (yes)": "result_high",
            "no": "result_med",
            "seemingly no": "result_med"
        }
    },

    # -------------------------
    # 7.4 (Inferential Stats - Right Column)
    # -------------------------
    "q_7_4_inf_r": {
        "question": "7.4. Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)? (E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test...)",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear (yes)"],
        "mapping": {
            "yes": "result_high",
            "seemingly yes": "result_high",
            "unclear (yes)": "result_high",
            "no": "result_high",
            "seemingly no": "result_high"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low": "LOW RISK",
    "result_med": "MEDIUM RISK",
    "result_high": "HIGH RISK"
}

TREES = {
    "1": decision_tree_1,
    "2": decision_tree_2,
    "3": decision_tree_3,
    "4": decision_tree_4,
    "5": decision_tree_5,
    "6": decision_tree_6,
    "7": decision_tree_7,
}