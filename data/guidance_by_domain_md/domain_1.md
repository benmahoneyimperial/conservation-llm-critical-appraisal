# Criterion 1: Risk of Confounding Biases

This criterion is concerned with biases due to uncontrolled (or inappropriately controlled) variable (confounder) that influences both the intervention/exposure and the outcome. We suggest assessors (and review teams) to complete Appendix A and develop a causal model before answering the checklist questions below to make assessment more objective.

# Answering the Checklist Questions

Please answer the checklist questions in Table B1 and record your responses.

Table B1. Checklist questions for risk of confounding biases.


| Category                                                                         | Checklist Questions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Answer (Tick One Applies)                                                 |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| General (please answer)                                                          | 1.1. Is it possible for the impact of the exposure or the effectiveness of the intervention to be confounded in this study? (E.g., Select Y/SY when randomisation is considered to deconfound.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No                                 |
| Conditional (answer if Y/SY to 1.1, otherwise select 'Not applicable')           | 1.2. Did the author(s) control for all the potential confounders? (All potential confounders should be listed in Appendix A.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable |
| Conditional (answer if N/SN/Unclear to 1.2, otherwise select 'Not applicable')   | 1.3. Is there any justifiable reason for not controlling for all the potential confounders (so that omission of some of the potential confounders is unlikely to influence the assessment of the effectiveness or impact)? (E.g., select Y/SY when there is evidence that omission of some of the potential confounders does not affect the assessment of effectiveness or impact. This may be the case if adjusting all potential confounders will lead to overadjustment, or an 'instrumental variable' is used for estimating the effectiveness or impact, etc. Instrumental variable is a variable that (1) is not associated with the confounder(s), (2) is associated with the intervention/exposure but (3) does not directly influence the outcome. If used appropriately, it enables valid estimation. See Hernán & Robins 2020 for guidance.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Not applicable                |
| Conditional (answer if Y/SY to 1.2 or 1.3, otherwise select 'Not applicable')    | 1.4. Were the potential confounders, that were controlled for, (and/or the instrumental variable used if applicable) likely to be measured accurately and precisely enough? (Measurements of factors may be nominal (categorical), ordinal (ranks) or scale.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable |
| Conditional (answer if you have answered 1.4, otherwise select 'Not applicable') | 1.5. Did the author(s) analyse the effect appropriately by taking into account the potential confounders, as well as the issue of accuracy and precision of the measurements of the potential confounders (and the instrumental variable if applicable)? (Examples of appropriate adjustment techniques for confounding may include stratification, matching, inverse probability weighting, standardisation, G-estimation, and instrumental variable estimation.)                                                                                                                                                                                                                                                                                                                                                                                      | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (No) ☐ Not applicable |


© 2021 the authors.

|  Optional (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible) | 1.6. What are the predicted magnitude and the direction of biases due to confounding? (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | □ Intervention or exposure intolerably favoured * □ Intervention or exposure tolerably favoured ** □ Comparator intolerably favoured * □ Comparator tolerably favoured ** □ Intolerably towards no effect * □ Tolerably towards no effect ** □ Intolerably away from no effect * □ Tolerably away from no effect ** □ Unpredictable □ Skip  |
| --- | --- | --- |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

Once you have answered the checklist questions, please use the diagram below (Figure B1) to finalise your judgement about risk of bias for this criterion.

```json
{ 
  "decisionTree": {
    "rootNode": "1.1",
    "nodes": [
      {
        "id": "1.1",
        "description": "Condition 1.1",
        "edges": [
          { "condition": "Yes", "target": "1.2" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "1.2",
        "description": "Condition 1.2",
        "edges": [
          { "condition": "Yes", "target": "1.4_A" },
          { "condition": "No", "target": "1.3" }
        ]
      },
      {
        "id": "1.3",
        "description": "Condition 1.3",
        "edges": [
          { "condition": "Yes", "target": "1.4_B" },
          { "condition": "No", "target": "High" }
        ]
      },
      {
        "id": "1.4_A",
        "description": "Condition 1.4 (Left Path)",
        "edges": [
          { "condition": "Yes", "target": "1.5_A" },
          { "condition": "No", "target": "1.5_A" }
        ]
      },
      {
        "id": "1.4_B",
        "description": "Condition 1.4 (Right Path)",
        "edges": [
          { "condition": "Yes", "target": "1.5_B" },
          { "condition": "No", "target": "1.5_B" }
        ]
      },
      {
        "id": "1.5_A",
        "description": "Condition 1.5 (Left Path)",
        "edges": [
          { "condition": "Yes", "target": "Low" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "1.5_B",
        "description": "Condition 1.5 (Right Path)",
        "edges": [
          { "condition": "Yes", "target": "Low" },
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
Figure B1. Roadmap diagram for making judgement about risk of confounding biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.

Please record your judgement about risk of bias for this criterion using Box B1 below.

Box B1. Judgement about risk of confounding biases.

|  □ Low risk of bias (reason for deviation from the suggested judgement: _____________________________)  |
| --- |
|  □ Medium risk of bias (reason for deviation from the suggested judgement: _____________________________)  |
|  □ High risk of bias (reason for deviation from the suggested judgement: _____________________________)  |

© 2021 the authors.