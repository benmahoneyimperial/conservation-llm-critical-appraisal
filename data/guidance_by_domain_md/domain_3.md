# Criterion 3: Risk of Misclassified Comparison Biases (Observational Studies Only)

This criterion is concerned with biases arising from misclassification or measurement of intervention, exposure and/or comparator.

# Answering the Checklist Questions

Please answer the checklist questions in Table B3 and record your responses.

Table B3. Checklist questions for risk of misclassified comparison biases.


| Category                                                                                      | Checklist Questions                                                                                                                                                                                                                                                                                                                                                          | Answer (Tick One Applies)                                                 |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Conditional (answer if type of the study is observational, otherwise select ‘not applicable’) | 3.1. Were the intervention or exposure (group) and the comparator (group) of interest sufficiently well-defined so that no meaningful vagueness remains for the intended assessment of causal effect of interest? (Select N/SN if the intervention/exposure and comparator of interest are vaguely or poorly defined. Such definitions may be provided in a study protocol.) | □ Yes □ Seemingly yes □ Seemingly no □ No □ Unclear (No) □ Not applicable |
| Conditional (answer if type of the study is                                                   | 3.2. Were the observed intervention or exposure (group) and the comparator (group) appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?                                                                                                                                                                                               | □ Yes □ Seemingly yes □ Seemingly no                                      |


© 2021 the authors.

|  observational, otherwise select 'not applicable') | (Select N/SN when measure or classification of exposure or intervention is unlikely to be accurate or precise enough, for example, when the use of an imprecise or inaccurate biomarker is used as a measure of exposure.) | ☐ No ☐ Unclear (No) ☐ Not applicable  |
| --- | --- | --- |
|  Conditional (answer if type of the study is observational, otherwise select 'not applicable') | 3.3. Might measure or classification of the observed exposure, intervention or comparator (group) have been incorrect due to error or influence of some knowledge, experience or desire? (Examples may include intentional misclassification of exposure to yield a desired outcome, unintentional misclassification due to prior knowledge or cognitive bias.) | ☐ Yes ☐ Seemingly yes ☐ Seemingly no ☐ No ☐ Unclear (Yes) ☐ Not applicable  |
|  Optional (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible. Select 'not applicable' if experimental treatments are applied.) | 3.4. What are the predicted magnitude and the direction of biases arising from misclassification or measurement of intervention, exposure and/or comparator? (Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.) | ☐ Intervention or exposure intolerably favoured * ☐ Intervention or exposure tolerably favoured ** ☐ Comparator intolerably favoured * ☐ Comparator tolerably favoured ** ☐ Intolerably towards no effect * ☐ Tolerably towards no effect ** ☐ Intolerably away from no effect * ☐ Tolerably away from no effect ** ☐ Unpredictable ☐ Not applicable ☐ Skip  |

* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias. ** Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.

Once you have answered the checklist questions, please use the diagram below (Figure B3) to finalise your judgement about risk of bias for this criterion.

© 2021 the authors.

```json
{
  "decisionTree": {
    "rootNode": "3.1",
    "nodes": [
      {
        "id": "3.1",
        "description": "Condition 3.1",
        "edges": [
          { "condition": "Yes", "target": "3.2_Left" },
          { "condition": "No", "target": "3.2_Right" }
        ]
      },
      {
        "id": "3.2_Left",
        "description": "Condition 3.2 (Left Branch)",
        "edges": [
          { "condition": "Yes", "target": "3.3_FarLeft" },
          { "condition": "No", "target": "3.3_Center" }
        ]
      },
      {
        "id": "3.2_Right",
        "description": "Condition 3.2 (Right Branch)",
        "edges": [
          { "condition": "Yes", "target": "3.3_Center" },
          { "condition": "No", "target": "3.3_FarRight" }
        ]
      },
      {
        "id": "3.3_FarLeft",
        "description": "Condition 3.3 (Far Left)",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "3.3_Center",
        "description": "Condition 3.3 (Center)",
        "edges": [
          { "condition": "Yes", "target": "High" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "3.3_FarRight",
        "description": "Condition 3.3 (Far Right)",
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
  }
}
```  
Figure B3. Roadmap diagram for making judgement about risk of misclassified comparison biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.

Please record your judgement about risk of bias for this criterion using Box B3 below.

Box B3. Judgement about risk of misclassified comparison biases.


| □ Low risk of bias (reason for deviation from the suggested judgement: _________________________)    |
| ---------------------------------------------------------------------------------------------------- |
| □ Medium risk of bias (reason for deviation from the suggested judgement: _________________________) |
| □ High risk of bias (reason for deviation from the suggested judgement: _________________________)   |
| □ Not applicable                                                                                     |
| Quantitative prediction of magnitude of bias (if available): _________________________               |


&nbsp;