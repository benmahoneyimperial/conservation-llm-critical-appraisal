# Criterion 6: Risk of Outcome Reporting Biases

This criterion is concerned with biases in reporting of study findings.

# Answering the Checklist Questions

Please answer the checklist questions in Table B6 and record your responses.

Table B6. Checklist questions for risk of outcome reporting biases.


| Category                | Checklist Questions                                                                                                                                                                                                                                                                                                                     | Answer (Tick One Applies)                                 |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| General (please answer) | 6.1. Are the reported relevant outcome data (or effect estimate) likely to be of (or based on) selected measurements of the outcome? (I.e., only a part of measured outcomes is reported. E.g., only 80 measured outcomes are reported when there are 100, or the effect estimate is based on 80 measured outcomes when there are 100.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) |
| General (please answer) | 6.2. Are relevant outcome data likely to be unreported for some subgroup(s)?                                                                                                                                                                                                                                                            | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) |


© 2021 the authors.

|   | (I.e., only outcome data on certain subjects or areas with certain characteristic(s) (e.g., taxonomic group) or in certain conditions (e.g., intervention intensity) are available.) |   |
| --- | --- | --- |
|  General (please answer) | 6.3. Is/are the analysis/analyses of the causal relationship of interest (intervention-outcome or exposure-outcome) likely to be partially reported? (I.e., there is/are other relevant analysis/analyses of the causal relationship that is/are not reported.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes)  |
|  Optional (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible) | 6.4. What are the predicted magnitude and the direction of biases in reporting of study findings? (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | ☐ Intervention or exposure intolerably favoured * ☐ Intervention or exposure tolerably favoured ** ☐ Comparator intolerably favoured * ☐ Comparator tolerably favoured ** ☐ Intolerably towards no effect * ☐ Tolerably towards no effect ** ☐ Intolerably away from no effect * ☐ Tolerably away from no effect ** ☐ Unpredictable ☐ Skip  |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

Once you have answered the checklist questions, please use the diagram below (Figure B6) to finalise your judgement about risk of bias for this criterion.

```json
{
  "decisionTree": {
    "rootNode": "6.1",
    "nodes": [
      {
        "id": "6.1",
        "description": "Condition 6.1",
        "edges": [
          { "condition": "Yes", "target": "6.2_Right" },
          { "condition": "No", "target": "6.2_Left" }
        ]
      },
      {
        "id": "6.2_Left",
        "description": "Condition 6.2 (Left)",
        "edges": [
          { "condition": "Yes", "target": "6.3_Center" },
          { "condition": "No", "target": "6.3_Left" }
        ]
      },
      {
        "id": "6.2_Right",
        "description": "Condition 6.2 (Right)",
        "edges": [
          { "condition": "Yes", "target": "6.3_Right" },
          { "condition": "No", "target": "6.3_Center" }
        ]
      },
      {
        "id": "6.3_Left",
        "description": "Condition 6.3 (Left)",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "6.3_Center",
        "description": "Condition 6.3 (Center)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "6.3_Right",
        "description": "Condition 6.3 (Right)",
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
Figure B6. Roadmap diagram for making judgement about risk of outcome reporting biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.

Please record your judgement about risk of bias for this criterion using Box B6 below.

Box B6. Judgement about risk of outcome reporting biases.


| □ Low risk of bias (reason for deviation from the suggested judgement: )    |
| --------------------------------------------------------------------------- |
| □ Medium risk of bias (reason for deviation from the suggested judgement: ) |
| □ High risk of bias (reason for deviation from the suggested judgement: )   |
| Quantitative prediction of magnitude of bias (if available):                |




&nbsp;