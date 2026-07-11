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
Roadmap diagram for making judgement about risk of performance biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.