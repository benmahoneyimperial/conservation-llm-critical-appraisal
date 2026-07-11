
### Criterion 5: Risk of Detection Biases

This criterion is concerned with biases arising from systematic differences in measurement of outcomes.

#### Answering the Checklist Questions

Please answer the checklist questions in Table B5 and record your responses.

**Table B5. Checklist questions for risk of detection biases.**

| Category | Checklist Questions | Answer (Tick One Applies) |
| :--- | :--- | :--- |
| **General** (please answer) | **5.1.** Was there any way for the outcome measure to be affected by knowledge of the exposure, intervention, subjects or areas, or desire for certain outcome?<br><br>*(E.g., select Y/SY if data collectors who measured the outcome or human subjects who report their outcomes were aware of the details of the study.)* | ☐ Yes<br>☐ Seemingly yes<br>☐ Seemingly no<br>☐ No<br>☐ Unclear (Yes) |
| **General** (please answer) | **5.2.** Was the measured outcome appropriate for the intended assessment of causal effect (i.e., causal effect of interest)?<br><br>*(E.g., select Y/SY if the measured outcome is consistent with the intended outcome; select N/SN if measured outcome is different from the pre-specified outcome or inappropriate for the intended assessment of causal effect.)* | ☐ Yes<br>☐ Seemingly yes<br>☐ Seemingly no<br>☐ No<br>☐ Unclear (No) |
| **General** (please answer) | **5.3.** Were the methods for measuring the outcome data the same across the groups?<br><br>*(E.g., select N/SN if the outcome was measured at different time windows between groups (e.g., 2 weeks after intervention vs. 4 weeks after control treatment). When exactly the same methods cannot be used among the groups due to the nature of the study, assessors may select Y/SY if the methods are sufficiently comparable. E.g., if a study measure bird species diversity in fields, and detectability of species is slightly different between groups but the slight difference in detectability can be considered comparable.)* | ☐ Yes<br>☐ Seemingly yes<br>☐ Seemingly no<br>☐ No<br>☐ Unclear (No) |
| **Conditional** (answer if N/SN/Unclear to 5.3) | **5.4.** Were the potential differences in measured outcomes between groups investigated and adjusted/corrected if necessary?<br><br>*(Differences in measured outcomes between groups can be a source of detection bias.)* | ☐ Yes<br>☐ Seemingly yes<br>☐ Seemingly no<br>☐ No<br>☐ Unclear (No)<br>☐ Not applicable |
| **Optional** (It is suggested that detailed rationale or empirical evidence be provided when predicting magnitude and direction of bias. Assessors may skip this optional checklist question if they feel unfeasible) | **5.4.** What are the predicted magnitude and the direction of biases arising from systematic differences in measurement of outcomes?<br><br>*(Note quantitative assessment (e.g., through simulation) may be conducted by risk-of-bias assessor(s) to predict the magnitude and direction of bias for this study result.)* | ☐ Intervention or exposure intolerably favoured \*<br>☐ Intervention or exposure tolerably favoured \*\*<br>☐ Comparator intolerably favoured \*<br>☐ Comparator tolerably favoured \*\*<br>☐ Intolerably towards no effect \*<br>☐ Tolerably towards no effect \*\*<br>☐ Intolerably away from no effect \*<br>☐ Tolerably away from no effect \*\*<br>☐ Unpredictable<br>☐ Skip |

*\* Intolerable means that the study result should not be considered as valid enough in relation to the predicted magnitude of bias.*
*\*\* Tolerable means that the study result could be considered as valid enough in relation to the predicted magnitude of bias.*

Once you have answered the checklist questions, please use the diagram below (Figure B5) to finalise your judgement about risk of bias for this criterion.


```json
{
  "decisionTree": {
    "rootNode": "5.1",
    "nodes": [
      {
        "id": "5.1",
        "description": "Condition 5.1",
        "edges": [
          { "condition": "Yes", "target": "5.2_Right" },
          { "condition": "No", "target": "5.2_Left" }
        ]
      },
      {
        "id": "5.2_Left",
        "description": "Condition 5.2 (Left)",
        "edges": [
          { "condition": "Yes", "target": "5.3_Left" },
          { "condition": "No", "target": "5.3_Right" }
        ]
      },
      {
        "id": "5.2_Right",
        "description": "Condition 5.2 (Right)",
        "edges": [
          { "condition": "Yes", "target": "5.3_Right" },
          { "condition": "No", "target": "5.3_Right" }
        ]
      },
      {
        "id": "5.3_Left",
        "description": "Condition 5.3 (Left)",
        "edges": [
          { "condition": "Yes", "target": "Low" },
          { "condition": "No", "target": "5.4" }
        ]
      },
      {
        "id": "5.3_Right",
        "description": "Condition 5.3 (Right)",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "5.4" }
        ]
      },
      {
        "id": "5.4",
        "description": "Condition 5.4",
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
**Figure B5.** Roadmap diagram for making judgement about risk of detection biases.

*Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.*

Please record your judgement about risk of bias for this criterion using Box B5 below.

**Box B5. Judgement about risk of detection biases.**
* [ ] Low risk of bias (reason for deviation from the suggested judgement: _______)
* [ ] Medium risk of bias (reason for deviation from the suggested judgement: _______)
* [ ] High risk of bias (reason for deviation from the suggested judgement: _______)

**Quantitative prediction of magnitude of bias (if available):** _______

