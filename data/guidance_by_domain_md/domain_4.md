# Criterion 4: Risk of Performance Biases (Experimental Studies Only)

This criterion is concerned with biases due to altered treatment procedure of interest.

# Answering the Checklist Questions

Please answer the checklist questions in Table B4 and record your responses.

Table B4. Checklist questions for risk of performance biases.


| Category                                                                                                    | Checklist Questions                                                                                                                                                                                                                                                                                                                                                                                                                           | Answer (Tick One Applies)                                                  |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Conditional (answer if experimental treatments are applied in the study, otherwise select ‘not applicable’) | 4.1. Were any of the persons, who applied or received treatments (intervention, exposure, alternative intervention, alternative exposure, or control), aware of the hypothesis that was being tested or the comparison that was being made? (Awareness of intervention, exposure, alternative intervention, alternative exposure or control treatment and the outcome of interest might be a factor that influences the treatment procedure.) | □ Yes □ Seemingly yes □ Seemingly no □ No □ Unclear (Yes) □ Not applicable |
| Conditional (answer if                                                                                      | 4.2. Were there any alterations of intervention/exposure or control treatments of interest that might have an impact on                                                                                                                                                                                                                                                                                                                       | □ Yes □ Seemingly yes                                                      |


© 2021 the authors.

|  experimental treatments are applied in the study, otherwise select 'not applicable') | the effectiveness of the intervention or the impact of the exposure? (Examples of alterations may include deviated initiation, implementation and/or discontinuation. E.g., select Y/SY if starting time for the intervention/exposure is deviated from a specified time window) | ☐ Seemingly no ☐ No ☐ Unclear (Yes) ☐ Not applicable  |
| --- | --- | --- |
|  Conditional (answer if Y/SY/Unclear to 4.2, otherwise select 'Not applicable') | 4.3. Were these deviated treatments unbalanced between intervention or exposure groups (when comparing two interventions or exposures), or inaccurately taken into account (when comparing intervention or exposure vs. control, and thus it might have influenced the estimate of impact or effectiveness? (E.g., select Y/SY when nitrogen fertilizer was mistakenly applied more than initially planned for one group, but this deviation is not reflected on the data collection sheet, i.e., not occurred as recorded.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) ☐ Not applicable  |
|  Conditional (answer if experimental treatments are applied in the study, otherwise select 'not applicable') | 4.4. Were both exposure/intervention and comparator treatments initiated and implemented as intended (or occurred as recorded) for all, or nearly all, subjects or areas? (When intervention, exposure, alternative intervention, alternative exposure or control treatment is not successful, it might be a source of performance bias.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable  |
|  Conditional (answer if Y/SY/Unclear to 4.2, or N/SN/Unclear to 4.4, otherwise select 'Not applicable') | 4.5. Are the used analysis methods of the impact of the exposure or the effectiveness of the intervention appropriate in relation to bias due to altered treatment procedure of interest? (E.g., select N/SN if the altered treatment procedure is not taken into account in the analysis.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable  |
|  Optional (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible. Select 'not applicable' if no experimental treatments are applied) | 4.6. What are the predicted magnitude and the direction of biases due to altered treatment procedure of interest? (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | ☐ Intervention or exposure intolerably favoured * ☐ Intervention or exposure tolerably favoured ** ☐ Comparator intolerably favoured * ☐ Comparator tolerably favoured ** ☐ Intolerably towards no effect * ☐ Tolerably towards no effect ** ☐ Intolerably away from no effect * ☐ Tolerably away from no effect ** ☐ Unpredictable ☐ Not applicable ☐ Skip  |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

© 2021 the authors.

Once you have answered the checklist questions, please use the diagram below (Figure B4) to finalise your judgement about risk of bias for this criterion.

```json
{
  "decisionTree": {
    "rootNode": "4.1",
    "nodes": [
      {
        "id": "4.1",
        "description": "Condition 4.1",
        "edges": [
          { "condition": "Yes", "target": "4.2_Center" },
          { "condition": "No", "target": "4.2_Left" }
        ]
      },
      {
        "id": "4.2_Left",
        "description": "Condition 4.2 (Left)",
        "edges": [
          { "condition": "Yes", "target": "4.3" },
          { "condition": "No", "target": "4.4_Left" }
        ]
      },
      {
        "id": "4.2_Center",
        "description": "Condition 4.2 (Center)",
        "edges": [
          { "condition": "Yes", "target": "4.3" },
          { "condition": "No", "target": "4.4_Left" }
        ]
      },
      {
        "id": "4.3",
        "description": "Condition 4.3",
        "edges": [
          { "condition": "Yes", "target": "4.4_Right" },
          { "condition": "No", "target": "4.4_Center" }
        ]
      },
      {
        "id": "4.4_Left",
        "description": "Condition 4.4 (Left)",
        "edges": [
          { "condition": "Yes", "target": "Low" },
          { "condition": "No", "target": "4.5_Center" }
        ]
      },
      {
        "id": "4.4_Center",
        "description": "Condition 4.4 (Center)",
        "edges": [
          { "condition": "Yes", "target": "4.5_Center" },
          { "condition": "No", "target": "4.5_Right" }
        ]
      },
      {
        "id": "4.4_Right",
        "description": "Condition 4.4 (Right)",
        "edges": [
          { "condition": "Yes", "target": "4.5_Right" },
          { "condition": "No", "target": "4.5_Right" }
        ]
      },
      {
        "id": "4.5_Center",
        "description": "Condition 4.5 (Center)",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "High" }
        ]
      },
      {
        "id": "4.5_Right",
        "description": "Condition 4.5 (Right)",
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
Figure B4. Roadmap diagram for making judgement about risk of performance biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.

Please record your judgement about risk of bias for this criterion using Box B4 below.

Box B4. Judgement about risk of performance biases.

Low risk of bias (reason for deviation from the suggested judgement:  
Medium risk of bias (reason for deviation from the suggested judgement:  
High risk of bias (reason for deviation from the suggested judgement:  
Not applicable Quantitative prediction of magnitude of bias (if available):

&nbsp;