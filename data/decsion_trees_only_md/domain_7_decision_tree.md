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
