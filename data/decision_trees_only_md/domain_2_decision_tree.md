```json
{
  "decisionTree": {
    "rootNode": "2.1",
    "nodes": [
      {
        "id": "2.1",
        "description": "Condition 2.1",
        "edges": [
          { "condition": "Yes", "target": "2.2_Left" },
          { "condition": "No", "target": "2.2_Right" }
        ]
      },
      {
        "id": "2.2_Left",
        "description": "Condition 2.2 (Left Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.3_Left" },
          { "condition": "No", "target": "2.3_Left" }
        ]
      },
      {
        "id": "2.2_Right",
        "description": "Condition 2.2 (Right Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.3_Right" },
          { "condition": "No", "target": "2.3_Right" }
        ]
      },
      {
        "id": "2.3_Left",
        "description": "Condition 2.3 (Left Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.4" },
          { "condition": "No", "target": "Low" }
        ]
      },
      {
        "id": "2.3_Right",
        "description": "Condition 2.3 (Right Branch)",
        "edges": [
          { "condition": "Yes", "target": "2.4" },
          { "condition": "No", "target": "2.4" }
        ]
      },
      {
        "id": "2.4",
        "description": "Condition 2.4",
        "edges": [
          { "condition": "Yes", "target": "Med" },
          { "condition": "No", "target": "2.5" }
        ]
      },
      {
        "id": "2.5",
        "description": "Condition 2.5",
        "edges": [
          { "condition": "Yes", "target": "2.6" },
          { "condition": "No", "target": "Med" }
        ]
      },
      {
        "id": "2.6",
        "description": "Condition 2.6",
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
Roadmap diagram for making judgement about risk of post-intervention/exposure selection biases. Note: if the optional question has been answered through quantitative assessment (e.g., through simulation), assessor's judgement about risk of bias for this criterion may be upgraded or downgraded from the suggested judgement, depending on result of quantitative assessment.