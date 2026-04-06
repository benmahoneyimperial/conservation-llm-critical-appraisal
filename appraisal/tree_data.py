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
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear", "not applicable"],
        "mapping": {
            "yes": "q_1_4_a",
            "seemingly yes": "q_1_4_a",
            "no": "q_1_3",
            "seemingly no": "q_1_3",
            "unclear": "q_1_3",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # 1.3
    # -------------------------
    "q_1_3": {
        "question": "1.3. Is there any justifiable reason for not controlling for all the potential confounders?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "not applicable"],
        "mapping": {
            "yes": "q_1_4_b",
            "seemingly yes": "q_1_4_b",
            "no": "result_high_risk_d",
            "seemingly no": "result_high_risk_d",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # 1.4 (Path A: from 1.2 YES)
    # -------------------------
    "q_1_4_a": {
        "question": "1.4. Were the potential confounders measured accurately and precisely enough?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear", "not applicable"],
        "mapping": {
            "yes": "q_1_5_a",
            "seemingly yes": "q_1_5_a",
            "no": "q_1_5_a",
            "seemingly no": "q_1_5_a",
            "unclear": "q_1_5_a",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # 1.5 (Path A)
    # -------------------------
    "q_1_5_a": {
        "question": "1.5. Did the author(s) analyse the effect appropriately taking confounders into account?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear", "not applicable"],
        "mapping": {
            "yes": "result_low_risk_b",
            "seemingly yes": "result_low_risk_b",
            "no": "result_medium_risk_c",
            "seemingly no": "result_medium_risk_c",
            "unclear": "result_medium_risk_c",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # 1.4 (Path B: from 1.3 YES)
    # -------------------------
    "q_1_4_b": {
        "question": "1.4. Were the potential confounders measured accurately and precisely enough?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear", "not applicable"],
        "mapping": {
            "yes": "q_1_5_b",
            "seemingly yes": "q_1_5_b",
            "no": "q_1_5_b",
            "seemingly no": "q_1_5_b",
            "unclear": "q_1_5_b",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # 1.5 (Path B)
    # -------------------------
    "q_1_5_b": {
        "question": "1.5. Did the author(s) analyse the effect appropriately taking confounders into account?",
        "valid_answers": ["yes", "seemingly yes", "seemingly no", "no", "unclear", "not applicable"],
        "mapping": {
            "yes": "result_low_risk_b",
            "seemingly yes": "result_low_risk_b",
            "no": "result_high_risk_d",
            "seemingly no": "result_high_risk_d",
            "unclear": "result_high_risk_d",
            "not applicable": "result_invalid_path"
        }
    },

    # -------------------------
    # RESULTS
    # -------------------------
    "result_low_risk_a": "LOW RISK: Confounding is not considered possible.",
    "result_low_risk_b": "LOW RISK: Confounders appropriately handled.",
    "result_medium_risk_c": "MEDIUM RISK: Analysis of confounders was not appropriate.",
    "result_high_risk_d": "HIGH RISK: Confounding not properly addressed.",
    
    # Safety catch
    "result_invalid_path": "ERROR: Invalid traversal (likely incorrect 'Not Applicable' usage)."
}

decision_tree_2 = {
    "start": {
        "question": "Question 2.1 (General): Selection and Exchangeability\nOption 2.1.a: Was the selection of subjects or areas after intervention or exposure random or systematic (i.e., based on random or systematic sampling), and exchangeability between groups could be assumed based on the selection approach?\n(Context): This applies when an attempt was not made to collect data of the entire, or nearly entire, population of inference. Exchangeability might be assumed if the two groups were exchangeable (i.e., comparable, the hypothetical effect estimate under the exchanged condition (i.e., swap) would not also be affected by post-intervention/exposure selection bias.\n\nOR\n\nOption 2.1.b: Was the entire (or nearly entire) population of inference followed-up after intervention or exposure, and exchangeability between before and after groups could be assumed?\n(Context): This applies when an attempt was made to collect data of the entire, or nearly entire, population of inference. Exchangeability might be assumed if the two groups were exchangeable (i.e., comparable, the hypothetical effect estimate under the exchanged condition (i.e., swap) would not also be affected by post-intervention/exposure selection bias.",
        "yes": "q_2_2_path_y",
        "no": "q_2_2_path_n"
    },
    # Path Y: 2.1 was Yes
    "q_2_2_path_y": {
        "question": "Question 2.2 (General): Blinding of Selection\nWas/were the researcher(s) unaware (or blinded) of the selection of subjects or areas?\n(Context): Non-blinding of selection might be a factor that influences the selection after intervention/exposure.",
        "yes": "q_2_3_path_y",
        "no": "q_2_3_path_y"
    },
    # Path N: 2.1 was No
    "q_2_2_path_n": {
        "question": "Question 2.2 (General): Blinding of Selection\nWas/were the researcher(s) unaware (or blinded) of the selection of subjects or areas?\n(Context): Non-blinding of selection might be a factor that influences the selection after intervention/exposure.",
        "yes": "q_2_3_path_n",
        "no": "q_2_3_path_n"
    },
    # Path Y: 2.1 Yes -> 2.3
    "q_2_3_path_y": {
        "question": "Question 2.3 (General): Exclusion or Loss After Intervention/Exposure\nAfter the start of the intervention/exposure or during the analysis, were any subjects or areas excluded or lost from the study or analysis?\n(Context): When some subjects or areas, or collected data are excluded, it might increase the risk of post-intervention/exposure selection bias.",
        "yes": "q_2_4",
        "no": "result_low_risk_a"
    },
    # Path N: 2.1 No -> 2.3
    "q_2_3_path_n": {
        "question": "Question 2.3 (General): Exclusion or Loss After Intervention/Exposure\nAfter the start of the intervention/exposure or during the analysis, were any subjects or areas excluded or lost from the study or analysis?\n(Context): When some subjects or areas, or collected data are excluded, it might increase the risk of post-intervention/exposure selection bias.",
        "yes": "q_2_4",
        "no": "q_2_4"
    },
    "q_2_4": {
        "question": "Question 2.4 (Conditional)\nWere the subjects or areas included in the study (or analysis) comparable between groups and so they allowed a valid comparison to be made (i.e., exchangeability or conditional exchangeability between groups could be assumed)?\n(Context): Select N/SN when groups are not comparable. For example, if the effect of air pollutants on plant growth to be studied, ‘resistance to pollutants’ may differ. ‘Less resistant’ individual plants may die, and ‘pollutant-resistant’ individuals may survive, and when only ‘pollutant-resistant’ individuals are included in the exposure group and both ‘less resistant’ and ‘pollutant-resistant’ individuals are included in the control group, the effect estimate may be biased. If only ‘pollutant-resistant’ individuals are selected in both groups, conditional exchangeability may hold.",
        "yes": "result_medium_risk_b",
        "no": "q_2_5"
    },
    "q_2_5": {
        "question": "Question 2.5 (Conditional)\nWere the difference(s) between groups likely to be explained by the intervention/exposure or a variable influenced by the intervention/exposure (including the outcome)?\n(Context): Note some variables influenced by the intervention or exposure might be unmeasured in the study. Such (unmeasured) variables are sometimes called latent variables.",
        "yes": "q_2_6",
        "no": "result_medium_risk_e"
    },
    "q_2_6": {
        "question": "Question 2.6 (Conditional)\nDid the author(s) adjust for the potential post-intervention/exposure selection bias in an appropriate way?\n(Context): E.g., stratification to pool stratum-specific outcomes.",
        "yes": "result_medium_risk_c",
        "no": "result_high_risk_d"
    },
    # Final Judgments
    "result_low_risk_a": "LOW RISK (Path A)",
    "result_medium_risk_b": "MEDIUM RISK (Path B)",
    "result_medium_risk_c": "MEDIUM RISK (Path C)",
    "result_high_risk_d": "HIGH RISK (Path D)",
    "result_medium_risk_e": "MEDIUM RISK (Path E)"
}

decision_tree_3 = {
    "start": {
        "question": "Domain 3 Applicability Check\n\nIs the study observational?\n\nIf the study is not observational (e.g., randomized controlled trial or other experimental study), select 'no'.",
        "yes": "q_3_1",
        "no": "result_na"
    },

    "q_3_1": {
        "question": "Question 3.1\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Were the intervention or exposure (group) and the comparator (group) of interest sufficiently well-defined so that no meaningful vagueness remains for the intended assessment of causal effect of interest?\n\n(Context): Select N/SN if the intervention/exposure and comparator of interest are vaguely or poorly defined. Such definitions may be provided in a study protocol.",
        "yes": "q_3_2_center",
        "no": "q_3_2_right"
    },

    # Path from 3.1 Yes
    "q_3_2_center": {
        "question": "Question 3.2\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Were the observed intervention or exposure (group) and the comparator (group) appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?\n\n(Context): Select N/SN when measure or classification of exposure or intervention is unlikely to be accurate or precise enough, for example, when the use of an imprecise or inaccurate biomarker is used as a measure of exposure.",
        "yes": "q_3_3_left",
        "no": "q_3_3_center"
    },

    # Path from 3.1 No
    "q_3_2_right": {
        "question": "Question 3.2\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Were the observed intervention or exposure (group) and the comparator (group) appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?\n\n(Context): Select N/SN when measure or classification of exposure or intervention is unlikely to be accurate or precise enough, for example, when the use of an imprecise or inaccurate biomarker is used as a measure of exposure.",
        "yes": "q_3_3_center",
        "no": "q_3_3_right"
    },

    # Path from 3.2 Center Yes
    "q_3_3_left": {
        "question": "Question 3.3\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?\n\n(Context): Examples may include intentional misclassification of exposure to yield a desired outcome, unintentional misclassification due to prior knowledge or cognitive bias.",
        "yes": "result_medium_risk",
        "no": "result_low_risk"
    },

    # Path from 3.2 Center No OR 3.2 Right Yes
    "q_3_3_center": {
        "question": "Question 3.3\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?\n\n(Context): Examples may include intentional misclassification of exposure to yield a desired outcome, unintentional misclassification due to prior knowledge or cognitive bias.",
        "yes": "result_high_risk",
        "no": "result_medium_risk"
    },

    # Path from 3.2 Right No
    "q_3_3_right": {
        "question": "Question 3.3\nCategory: Conditional (answer if type of the study is observational, otherwise select ‘not applicable’)\n\nQuestion: Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire?\n\n(Context): Examples may include intentional misclassification of exposure to yield a desired outcome, unintentional misclassification due to prior knowledge or cognitive bias.",
        "yes": "result_high_risk",
        "no": "result_medium_risk"
    },

    # Final Judgments
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK",
    "result_na": "NOT APPLICABLE"
}

decision_tree_4 = {
    "start": {
        "question": "Domain 4 Applicability Check\n\nDoes the study apply experimental treatments (i.e., interventions actively applied by researchers)?\n\nIf the study is purely observational and does not apply experimental treatments, select 'no'.",
        "yes": "q_4_1",
        "no": "result_na"
    },

    "q_4_1": {
        "question": "Question 4.1\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were any of the persons, who applied or received treatments (intervention, exposure, alternative intervention, alternative exposure, or control), aware of the hypothesis that was being tested or the comparison that was being made?\n\n(Context): Awareness of intervention, exposure, alternative intervention, alternative exposure or control treatment and the outcome of interest might be a factor that influences the treatment procedure.",
        "yes": "q_4_2_center",
        "no": "q_4_2_left"
    },

    # 4.2 Left (from 4.1 No)
    "q_4_2_left": {
        "question": "Question 4.2\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were there any alterations of intervention/exposure or control treatments of interest that might have an impact on the effectiveness of the intervention or the impact of the exposure?\n\n(Context): Examples of alterations may include deviated initiation, implementation and/or discontinuation. E.g., select Y/SY if starting time for the intervention/exposure is deviated from a specified time window.",
        "yes": "q_4_3_center",
        "no": "q_4_4_far_left"
    },

    # 4.2 Center (from 4.1 Yes)
    "q_4_2_center": {
        "question": "Question 4.2\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were there any alterations of intervention/exposure or control treatments of interest that might have an impact on the effectiveness of the intervention or the impact of the exposure?\n\n(Context): Examples of alterations may include deviated initiation, implementation and/or discontinuation. E.g., select Y/SY if starting time for the intervention/exposure is deviated from a specified time window.",
        "yes": "q_4_3_center",
        "no": "q_4_4_center"
    },

    # 4.3 Center
    "q_4_3_center": {
        "question": "Question 4.3\nCategory: Conditional (answer if Y/SY/Unclear to 4.2, otherwise select 'Not applicable')\n\nQuestion: Were these deviated treatments unbalanced between intervention or exposure groups (when comparing two interventions or exposures), or inaccurately taken into account (when comparing intervention or exposure vs. control, and thus it might have influenced the estimate of impact or effectiveness?\n\n(Context): E.g., select Y/SY when nitrogen fertilizer was mistakenly applied more than initially planned for one group, but this deviation is not reflected on the data collection sheet, i.e., not occurred as recorded.",
        "yes": "q_4_4_far_right",
        "no": "q_4_4_center"
    },

    # 4.4 Far Left
    "q_4_4_far_left": {
        "question": "Question 4.4\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?\n\n(Context): When intervention, exposure, alternative intervention, alternative exposure or control treatment is not successful, it might be a source of performance bias.",
        "yes": "result_low_risk",
        "no": "q_4_5_center"
    },

    # 4.4 Center
    "q_4_4_center": {
        "question": "Question 4.4\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?\n\n(Context): When intervention, exposure, alternative intervention, alternative exposure or control treatment is not successful, it might be a source of performance bias.",
        "yes": "q_4_5_center",
        "no": "q_4_5_far_right"
    },

    # 4.4 Far Right
    "q_4_4_far_right": {
        "question": "Question 4.4\nCategory: Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’)\n\nQuestion: Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas?\n\n(Context): When intervention, exposure, alternative intervention, alternative exposure or control treatment is not successful, it might be a source of performance bias.",
        "yes": "q_4_5_far_right",
        "no": "q_4_5_far_right"
    },

    # 4.5 Center
    "q_4_5_center": {
        "question": "Question 4.5\nCategory: Conditional (answer if Y/SY/Unclear to 4.2, or N/SN/Unclear to 4.4, otherwise select 'Not applicable')\n\nQuestion: Are the used analysis methods of the impact of the exposure or the effectiveness of the intervention appropriate in relation to bias due to altered treatment procedure of interest?\n\n(Context): E.g., select N/SN if the altered treatment procedure is not taken into account in the analysis.",
        "yes": "result_medium_risk",
        "no": "result_high_risk"
    },

    # 4.5 Far Right
    "q_4_5_far_right": {
        "question": "Question 4.5\nCategory: Conditional (answer if Y/SY/Unclear to 4.2, or N/SN/Unclear to 4.4, otherwise select 'Not applicable')\n\nQuestion: Are the used analysis methods of the impact of the exposure or the effectiveness of the intervention appropriate in relation to bias due to altered treatment procedure of interest?\n\n(Context): E.g., select N/SN if the altered treatment procedure is not taken into account in the analysis.",
        "yes": "result_medium_risk",
        "no": "result_high_risk"
    },

    # Final Judgments
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK",
    "result_na": "NOT APPLICABLE"
}


decision_tree_5 = {
    "start": {
        "question": "Question 5.1\nCategory: General (please answer)\n\nQuestion: Was there any way for the outcome measure to be affected by knowledge of the exposure, intervention, subjects or areas, or desire for certain outcome?\n\n(Context): E.g., select Y/SY if data collectors who measured the outcome or human subjects who report their outcomes were aware of the details of the study.",
        "yes": "q_5_2_right",
        "no": "q_5_2_left"
    },
    # Path from 5.1 No (Left)
    "q_5_2_left": {
        "question": "Question 5.2\nCategory: General (please answer)\n\nQuestion: Was the measured outcome appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?\n\n(Context): E.g., select Y/SY if the measured outcome is consistent with the intended outcome; select N/SN if measured outcome is different from the pre-specified outcome or inappropriate for the intended assessment of causal effect.",
        "yes": "q_5_3_left",
        "no": "q_5_3_right"
    },
    # Path from 5.1 Yes (Right)
    "q_5_2_right": {
        "question": "Question 5.2\nCategory: General (please answer)\n\nQuestion: Was the measured outcome appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?\n\n(Context): E.g., select Y/SY if the measured outcome is consistent with the intended outcome; select N/SN if measured outcome is different from the pre-specified outcome or inappropriate for the intended assessment of causal effect.",
        "yes": "q_5_3_right",
        "no": "q_5_3_right"
    },
    # Path from 5.2 Left Yes
    "q_5_3_left": {
        "question": "Question 5.3\nCategory: General (please answer)\n\nQuestion: Were the methods for measuring the outcome data the same across the groups?\n\n(Context): E.g., select N/SN if the outcome was measured at different time windows between groups (e.g., 2 weeks after intervention vs. 4 weeks after control treatment). When exactly the same methods cannot be used among the groups due to the nature of the study, assessors may select Y/SY if the methods are sufficiently comparable. E.g., if a study measure bird species diversity in fields, and detectability of species is slightly different between groups but the slight difference in detectability can be considered comparable.",
        "yes": "result_low_risk",
        "no": "q_5_4"
    },
    # Path from 5.2 Left No OR 5.2 Right Yes/No
    "q_5_3_right": {
        "question": "Question 5.3\nCategory: General (please answer)\n\nQuestion: Were the methods for measuring the outcome data the same across the groups?\n\n(Context): E.g., select N/SN if the outcome was measured at different time windows between groups (e.g., 2 weeks after intervention vs. 4 weeks after control treatment). When exactly the same methods cannot be used among the groups due to the nature of the study, assessors may select Y/SY if the methods are sufficiently comparable. E.g., if a study measure bird species diversity in fields, and detectability of species is slightly different between groups but the slight difference in detectability can be considered comparable.",
        "yes": "result_medium_risk",
        "no": "q_5_4"
    },
    # Path from 5.3 Left No OR 5.3 Right No
    "q_5_4": {
        "question": "Question 5.4\nCategory: Conditional (answer if N/SN/Unclear to 5.3)\n\nQuestion: Were the potential differences in measured outcomes between groups investigated and adjusted/corrected if necessary?\n\n(Context): Differences in measured outcomes between groups can be a source of detection bias.",
        "yes": "result_medium_risk",
        "no": "result_high_risk"
    },
    # Final Judgments
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK"
}

decision_tree_6 = {
    "start": {
        "question": "Question 6.1\nCategory: General (please answer)\n\nQuestion: Are the reported relevant outcome data (or effect estimate) likely to be of (or based on) selected measurements of the outcome?\n\n(Context): I.e., only a part of measured outcomes is reported. E.g., only 80 measured outcomes are reported when there are 100, or the effect estimate is based on 80 measured outcomes when there are 100.",
        "yes": "q_6_2_right",
        "no": "q_6_2_left"
    },
    # 6.2 Left (from 6.1 No)
    "q_6_2_left": {
        "question": "Question 6.2\nCategory: General (please answer)\n\nQuestion: Are relevant outcome data likely to be unreported for some subgroup(s)?\n\n(Context): I.e., only outcome data on certain subjects or areas with certain characteristic(s) (e.g., taxonomic group) or in certain conditions (e.g., intervention intensity) are available.",
        "yes": "q_6_3_center",
        "no": "q_6_3_left"
    },
    # 6.2 Right (from 6.1 Yes)
    "q_6_2_right": {
        "question": "Question 6.2\nCategory: General (please answer)\n\nQuestion: Are relevant outcome data likely to be unreported for some subgroup(s)?\n\n(Context): I.e., only outcome data on certain subjects or areas with certain characteristic(s) (e.g., taxonomic group) or in certain conditions (e.g., intervention intensity) are available.",
        "yes": "q_6_3_right",
        "no": "q_6_3_center"
    },
    # 6.3 Left (from 6.2 Left No)
    "q_6_3_left": {
        "question": "Question 6.3\nCategory: General (please answer)\n\nQuestion: Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported?\n\n(Context): I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.",
        "yes": "result_medium_risk",
        "no": "result_low_risk"
    },
    # 6.3 Center (from 6.2 Left Yes OR 6.2 Right No)
    "q_6_3_center": {
        "question": "Question 6.3\nCategory: General (please answer)\n\nQuestion: Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported?\n\n(Context): I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.",
        "yes": "result_high_risk",
        "no": "result_medium_risk"
    },
    # 6.3 Right (from 6.2 Right Yes)
    "q_6_3_right": {
        "question": "Question 6.3\nCategory: General (please answer)\n\nQuestion: Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported?\n\n(Context): I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.",
        "yes": "result_high_risk",
        "no": "result_high_risk"
    },
    # Final Judgments
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK"
}

decision_tree_7 = {
    "start": {
        "question": "Question 7.0\nCategory: Preliminary\n\nQuestion: Are inferential statistics applied in this study?\n\n(Context): Inferential statistics include null hypothesis testing, estimation, confidence intervals, etc. If no, we assess based on descriptive statistics only.",
        "yes": "q_7_1_B", # Tree B (Conducted)
        "no": "q_7_1_A"  # Tree A (Not Conducted)
    },
    # --- Tree A (No Inferential Statistics) ---
    "q_7_1_A": {
        "question": "Question 7.1\nCategory: General (please answer)\n\nQuestion: Was/were the person(s), who estimated the effectiveness of the intervention or the impact of the exposure, aware of the exposure or intervention received by subjects or areas?\n\n(Context): E.g., select Y/SY if analysts were aware of the details of the study.",
        "yes": "q_7_2_right_A",
        "no": "q_7_2_left_A"
    },
    "q_7_2_left_A": {
        "question": "Question 7.2\nCategory: General (please answer)\n\nQuestion: Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses?\n\n(Context): E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.",
        "yes": "result_medium_risk",
        "no": "result_low_risk"
    },
    "q_7_2_right_A": {
        "question": "Question 7.2\nCategory: General (please answer)\n\nQuestion: Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses?\n\n(Context): E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.",
        "yes": "result_high_risk",
        "no": "result_medium_risk"
    },

    # --- Tree B (Inferential Statistics Conducted) ---
    "q_7_1_B": {
        "question": "Question 7.1\nCategory: General (please answer)\n\nQuestion: Was/were the person(s), who estimated the effectiveness of the intervention or the impact of the exposure, aware of the exposure or intervention received by subjects or areas?\n\n(Context): E.g., select Y/SY if analysts were aware of the details of the study.",
        "yes": "q_7_2_right_B",
        "no": "q_7_2_left_B"
    },
    # 7.2 Left B (from 7.1 No)
    "q_7_2_left_B": {
        "question": "Question 7.2\nCategory: General (please answer)\n\nQuestion: Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses?\n\n(Context): E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.",
        "yes": "q_7_3_far_right",
        "no": "q_7_3_left"
    },
    # 7.2 Right B (from 7.1 Yes)
    "q_7_2_right_B": {
        "question": "Question 7.2\nCategory: General (please answer)\n\nQuestion: Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses?\n\n(Context): E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.",
        "yes": "q_7_3_far_right",
        "no": "q_7_3_center"
    },
    
    # 7.3 Left (from 7.2 Left B No)
    "q_7_3_left": {
        "question": "Question 7.3\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)?\n\n(Context): E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.",
        "yes": "q_7_4_far_right",
        "no": "q_7_4_left"
    },
    # 7.3 Center (from 7.2 Right B No)
    "q_7_3_center": {
        "question": "Question 7.3\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)?\n\n(Context): E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.",
        "yes": "q_7_4_far_right",
        "no": "q_7_4_center"
    },
    # 7.3 Far Right (from 7.2 Left B Yes OR 7.2 Right B Yes)
    "q_7_3_far_right": {
        "question": "Question 7.3\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)?\n\n(Context): E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.",
        "yes": "result_high_risk",
        "no": "q_7_4_far_right"
    },

    # 7.4 Left (from 7.3 Left No)
    "q_7_4_left": {
        "question": "Question 7.4\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)?\n\n(Context): E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test, equal or unequal variances not tested when testing for a difference, no justification for the choice of dependent and independent variables, a Pearson’s correlation test was used when analysing a causal relationship, inappropriate comparison of multiple models to support the provided statement when some of the models do not relate to impact or effectiveness, inappropriate modelling which may affect an estimate of effectiveness or impact.",
        "yes": "result_medium_risk",
        "no": "result_low_risk"
    },
    # 7.4 Center (from 7.3 Center No)
    "q_7_4_center": {
        "question": "Question 7.4\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)?\n\n(Context): E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test, equal or unequal variances not tested when testing for a difference, no justification for the choice of dependent and independent variables, a Pearson’s correlation test was used when analysing a causal relationship, inappropriate comparison of multiple models to support the provided statement when some of the models do not relate to impact or effectiveness, inappropriate modelling which may affect an estimate of effectiveness or impact.",
        "yes": "result_high_risk",
        "no": "result_medium_risk"
    },
    # 7.4 Far Right (from 7.3 Left Yes OR 7.3 Center Yes OR 7.3 Far Right No)
    "q_7_4_far_right": {
        "question": "Question 7.4\nCategory: Conditional (answer if inferential statistics are applied, otherwise select ‘not applicable’)\n\nQuestion: Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)?\n\n(Context): E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test, equal or unequal variances not tested when testing for a difference, no justification for the choice of dependent and independent variables, a Pearson’s correlation test was used when analysing a causal relationship, inappropriate comparison of multiple models to support the provided statement when some of the models do not relate to impact or effectiveness, inappropriate modelling which may affect an estimate of effectiveness or impact.",
        "yes": "result_high_risk",
        "no": "result_high_risk"
    },

    # Final Judgments
    "result_low_risk": "LOW RISK",
    "result_medium_risk": "MEDIUM RISK",
    "result_high_risk": "HIGH RISK"
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