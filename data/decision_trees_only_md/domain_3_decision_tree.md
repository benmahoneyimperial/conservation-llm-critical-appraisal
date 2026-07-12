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
Roadmap diagram for making judgement about risk of misclassified comparison biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.
