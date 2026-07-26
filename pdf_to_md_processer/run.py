from pathlib import Path
from datalab_sdk import DatalabClient
import json

# ----------------------------
# Configuration
# ----------------------------

INPUT_FOLDER = Path("data/papers/papers_pdf/test_5")
OUTPUT_FOLDER = Path("data/papers/papers_md/test_extraction_md")

PIPELINE_ID = "pl_DaOCkFJs7xHv"
PIPELINE_VERSION = 3

OUTPUT_FOLDER.mkdir(exist_ok=True)

client = DatalabClient(api_key="YTzF4AGDlntoM8Xepa2YBtMpV58h2gLBZq7F4Lr_qS4")


# ----------------------------
# Process PDFs
# ----------------------------

for pdf in INPUT_FOLDER.glob("*.pdf"):

    print(f"Processing {pdf.name}...")

    try:
        execution = client.run_pipeline(
            pipeline_id=PIPELINE_ID,
            version=PIPELINE_VERSION,
            file_path=pdf,
            max_polls=60,
            poll_interval=5,
        )

        if execution.status != "completed":
            raise Exception(f"Pipeline failed: {execution.status}")

        # Extract JSON result from extraction step
        result = client.get_step_result(
            execution.execution_id,
            step_index=1
        )

        # Save JSON
        output_file = OUTPUT_FOLDER / f"{pdf.stem}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved {output_file.name}")

    except Exception as e:
        print(f"✗ Failed {pdf.name}: {e}")

print("Done!")