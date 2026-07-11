# Criterion 2: Risk of Post-Intervention/Exposure Selection Biases

This criterion is concerned with biases arising from systematic differences in the selection of subjects or areas into the study or analysis after intervention or exposure.

# Answering the Checklist Questions

Please answer the checklist questions in Table B2 and record your responses.

Table B2. Checklist questions for risk of post-intervention/exposure selection biases.


| Category                                   | Checklist Questions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Answer (Tick One Applies)                                 |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| General (please answer whichever suitable) | 2.1.a. Was the selection of subjects or areas after intervention or exposure random or systematic (i.e., based on random or systematic sampling), and exchangeability between groups could be assumed based on the selection approach? (This applies when an attempt was not made to collect data of the entire, or nearly entire, population of inference. Exchangeability might be assumed if the two groups were exchangeable (i.e., comparable, the hypothetical effect estimate under the exchanged condition (i.e., swap) would not also be affected by post-intervention/exposure selection bias.) OR 2.1.b. Was the entire (or nearly entire) population of inference followed-up after intervention or exposure, and exchangeability between before and after groups could be assumed? (This applies when an attempt was made to collect data of the entire, or nearly entire, population of inference. Exchangeability might be assumed if the two groups were exchangeable (i.e., comparable, the hypothetical effect estimate under the exchanged condition (i.e., swap) would not also be affected by post-intervention/exposure selection bias.) | ☐ Answer 2.1.a ☐ Answer 2.1.b                             |
| &nbsp;                                     | &nbsp;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No)  |
| General (please answer)                    | 2.2. Was/were the researcher(s) unaware (or blinded) of the selection of subjects or areas? (Non-blinding of selection might be a factor that influences the selection after intervention/exposure.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No)  |
| General (please answer)                    | 2.3. After the start of the intervention/exposure or during the analysis, were any subjects or areas excluded or lost from the study or analysis? (When some subjects or areas, or collected data are excluded, it might increase the risk of post-intervention/exposure selection bias.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) |


© 2021 the authors.

|  Conditional (answer if N/SN/Unclear to 2.1, or Y/SY/Unclear to 2.3, otherwise select 'Not applicable') | 2.4. Were the subjects or areas included in the study (or analysis) comparable between groups and so they allowed a valid comparison to be made (i.e., exchangeability or conditional exchangeability between groups could be assumed)? (Select N/SN when groups are not comparable. For example, if the effect of air pollutants on plant growth to be studied, 'resistance to pollutants' may differ. 'Less resistant' individual plants may die, and 'pollutant-resistant' individuals may survive, and when only 'pollutant-resistant' individuals are included in the exposure group and both 'less resistant' and 'pollutant-resistant' individuals are included in the control group, the effect estimate may be biased. If only 'pollutant-resistant' individuals are selected in both groups, conditional exchangeability may hold.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable  |
| --- | --- | --- |
|  Conditional (answer if N/SN/Unclear to 2.4, otherwise select 'Not applicable') | 2.5. Were the difference(s) between groups likely to be explained by the intervention/exposure or a variable influenced by the intervention/exposure (including the outcome)? (Note some variables influenced by the intervention or exposure might be unmeasured in the study. Such (unmeasured) variables are sometimes called latent variables.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) ☐ Not applicable  |
|  Conditional (answer if Y/SY/Unclear to 2.5, otherwise select 'Not applicable') | 2.6. Did the author(s) adjust for the potential post-intervention/exposure selection bias in an appropriate way? (E.g., stratification to pool stratum-specific outcomes) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable  |
|  Optional (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible) | 2.7. What are the predicted magnitude and the direction of biases arising from systematic differences in the selection of subjects or areas into the study or analysis after intervention or exposure? (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | ☐ Intervention or exposure intolerably favoured * ☐ Intervention or exposure tolerably favoured ** ☐ Comparator intolerably favoured * ☐ Comparator tolerably favoured ** ☐ Intolerably towards no effect * ☐ Tolerably towards no effect ** ☐ Intolerably away from no effect * ☐ Tolerably away from no effect ** ☐ Unpredictable ☐ Skip  |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

Once you have answered the checklist questions, please use the diagram below (Figure B2) to finalise your judgement about risk of bias for this criterion.

© 2021 the authors.

```json
{
  "decisionTree": {
    "rootNode": "2.1",
    "nodes": [
      {
        "id": "2.1",
        "description": "Condition 2.1",
        "edges": [
          { "condition": "Yes", "target": "2.2_Left" },
          { "condition": "No", "target": "2.2_Right" }
        ]
      },
      {
        "id": "2.2_Left",
        "description": "Condition 2.2 (Left Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.3_Left" },
          { "condition": "No", "target": "2.3_Left" }
        ]
      },
      {
        "id": "2.2_Right",
        "description": "Condition 2.2 (Right Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.3_Right" },
          { "condition": "No", "target": "2.3_Right" }
        ]
      },
      {
        "id": "2.3_Left",
        "description": "Condition 2.3 (Left Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.4" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "2.3_Right",
        "description": "Condition 2.3 (Right Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.4" },
          { "condition": "No", "target": "2.4" }
        ]
      },
      {
        "id": "2.4",
        "description": "Condition 2.4",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "2.5" }
        ]
      },
      {
        "id": "2.5",
        "description": "Condition 2.5",
        "edges": [
          { "condition": "Yes", "target": "2.6" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "2.6",
        "description": "Condition 2.6",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "High" }
        ]
      }
    ],
    "leaves": [
      { "id": "Low", "value": "Low" },
      { "id": "Med", "value": "Med" },
      { "id": "High", "value": "High" }
    ]
  }
}
```  
Figure B2. Roadmap diagram for making judgement about risk of post-intervention/exposure selection biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.

Please record your judgement about risk of bias for this criterion using Box B2 below.

Box B2. Judgement about risk of post-intervention/exposure selection biases.


| □ Low risk of bias (reason for deviation from the suggested judgement: _________________________)    |
| ---------------------------------------------------------------------------------------------------- |
| □ Medium risk of bias (reason for deviation from the suggested judgement: _________________________) |
| □ High risk of bias (reason for deviation from the suggested judgement: _________________________)   |
| Quantitative prediction of magnitude of bias (if available): _________________________               |




&nbsp;