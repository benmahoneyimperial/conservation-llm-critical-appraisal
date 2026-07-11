# Criterion 7: Risk of Outcome Assessment Biases

This criterion is concerned with biases due to error in applied statistical methods.

# Answering the Checklist Questions

Please answer the checklist questions in Table B7 and record your responses.

Table B7. Checklist questions for risk of outcome assessment biases.


| Category                                                                                      | Checklist Questions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Answer (Tick One Applies)                                      |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| General (please answer)                                                                       | 7.1. Was/were the person(s), who estimated the effectiveness of the intervention or the impact of the exposure, aware of the exposure or intervention received by subjects or areas? (E.g., select Y/SY if analysts were aware of the details of the study.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Yes Seemingly yes Seemingly no No Unclear (Yes)                |
| General (please answer)                                                                       | 7.2. Is it likely that there is/are error(s) or inappropriate methods in the applied descriptive statistical analyses? (E.g., miscalculations of sample sizes, means, medians, variances, ranges for intervention/exposure and comparator groups, error in converting analogue to digital data.)                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Yes Seemingly yes Seemingly no No Unclear (Yes)                |
| Conditional (answer if inferential statistics are applied, otherwise select 'not applicable') | 7.3. Is it likely that there is/are error(s) in the applied inferential statistics (including null hypothesis testing, estimation, coding)? (E.g., miscalculations of differences between intervention/exposure and comparator, errors in coding, etc.)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Yes Seemingly yes Seemingly no No Unclear (Yes) Not applicable |
| Conditional (answer if inferential statistics are applied, otherwise select 'not applicable') | 7.4. Were assumptions for the applied inferential statistics violated or the applied inferential statistical methods inappropriate for the inferential goal(s)? (E.g., use of inappropriate sample sizes to test the hypothesis, normality not assumed when conducting a parametric test, equal or unequal variances not tested when testing for a difference, no justification for the choice of dependent and independent variables, a Pearson's correlation test was used when analysing a causal relationship, inappropriate comparison of multiple models to support the provided statement when some of the models do not relate to impact or effectiveness, inappropriate modelling which may affect an estimate of effectiveness or impact.) | Yes Seemingly yes Seemingly no No Unclear (Yes) Not applicable |
| Optional (It is suggested that                                                                | 7.5. What are the predicted magnitude and the direction of biases due to error in applied statistical methods?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Intervention or exposure intolerably favoured *                |
| in the applied descriptive statistical analysis)                                              | &nbsp;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | &nbsp;                                                         |


© 2021 the authors.

|  detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible) | (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | □ Intervention or exposure tolerably favoured ** □ Comparator intolerably favoured * □ Comparator tolerably favoured ** □ Intolerably towards no effect * □ Tolerably towards no effect ** □ Intolerably away from no effect * □ Tolerably away from no effect ** □ Unpredictable □ Skip  |
| --- | --- | --- |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

Once you have answered the checklist questions, please use the diagram below (Figure B7) to finalise your judgement about risk of bias for this criterion.

```json
{
  "decisionTree7_A": {
    "context": "Inferential statistics not conducted",
    "rootNode": "7.1",
    "nodes": [
      {
        "id": "7.1",
        "description": "Condition 7.1",
        "edges": [
          { "condition": "Yes", "target": "7.2_Right" },
          { "condition": "No", "target": "7.2_Left" }
        ]
      },
      {
        "id": "7.2_Left",
        "description": "Condition 7.2 (Left)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "7.2_Right",
        "description": "Condition 7.2 (Right)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Med" }
        ]
      }
    ],
    "leaves": [
      { "id": "Low", "value": "Low" },
      { "id": "Med", "value": "Med" },
      { "id": "High", "value": "High" }
    ]
  },
  "decisionTree7_B": {
    "context": "Inferential statistics conducted",
    "rootNode": "7.1",
    "nodes": [
      {
        "id": "7.1",
        "description": "Condition 7.1",
        "edges": [
          { "condition": "Yes", "target": "7.2_Right" },
          { "condition": "No", "target": "7.2_Left" }
        ]
      },
      {
        "id": "7.2_Left",
        "description": "Condition 7.2 (Left)",
        "edges": [
          { "condition": "Yes", "target": "7.3_Right" },
          { "condition": "No", "target": "7.3_Left" }
        ]
      },
      {
        "id": "7.2_Right",
        "description": "Condition 7.2 (Right)",
        "edges": [
          { "condition": "Yes", "target": "7.3_Right" },
          { "condition": "No", "target": "7.3_Center" }
        ]
      },
      {
        "id": "7.3_Left",
        "description": "Condition 7.3 (Left)",
        "edges": [
          { "condition": "Yes", "target": "7.4_Right" },
          { "condition": "No", "target": "7.4_Left" }
        ]
      },
      {
        "id": "7.3_Center",
        "description": "Condition 7.3 (Center)",
        "edges": [
          { "condition": "Yes", "target": "7.4_Right" },
          { "condition": "No", "target": "7.4_Center" }
        ]
      },
      {
        "id": "7.3_Right",
        "description": "Condition 7.3 (Right)",
        "edges": [
          { "condition": "Yes", "target": "7.4_Right" },
          { "condition": "No", "target": "7.4_Right" }
        ]
      },
      {
        "id": "7.4_Left",
        "description": "Condition 7.4 (Left)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "7.4_Center",
        "description": "Condition 7.4 (Center)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "7.4_Right",
        "description": "Condition 7.4 (Right)",
        "edges": [
          { "condition": "Yes", "target": "High" },
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
Figure B7. Roadmap diagram for making judgement about risk of outcome assessment biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.


Please record your judgement about risk of biases for this criterion using Box B7 below.

Box B7. Judgement about risk of outcome assessment biases.

|  □ Low risk of bias (reason for deviation from the suggested judgement: _____________________________)  |
| --- |
|  □ Medium risk of bias (reason for deviation from the suggested judgement: _____________________________)  |
|  □ High risk of bias (reason for deviation from the suggested judgement: _____________________________)  |
|  Quantitative prediction of magnitude of bias (if available): _____________________________  |

