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
Roadmap diagram for making judgement about risk of performance biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.
