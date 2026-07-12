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
Roadmap diagram for making judgement about risk of outcome reporting biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.
