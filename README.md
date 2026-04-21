# conservation-llm-critical-appraisal
Benchmarking Large Language Models (LLMs) against human experts for critical appraisal of conservation literature using the CEECAT framework

## Project layout

- `appraisal/`: decision-tree appraisal system based on CEECAT domain trees.
- `single_shot/`: separate single-prompt appraisal system.
- `benchmarking/`: benchmark runner for comparing expected and actual domain outcomes.
- `preprocessing/`: PDF-to-Markdown extraction and Methods/Results section utilities.
- `scripts/`: command-line entry points for the main workflows.
- `data/`: benchmark data, processed paper text, and guidance assets.

## Main entry points

- `scripts/run_appraisal.py`: run the decision-tree appraisal pipeline on one paper or a directory of processed text files.
- `scripts/run_single_appraisal.py`: inspect a single paper with full decision-tree trace output.
- `scripts/run_single_shot.py`: run the separate single-shot appraisal workflow.
- `scripts/extract_methods_results_markdown.py`: convert PDFs to Markdown with MarkItDown, then write Methods/Results-only Markdown files.
- `benchmarking/evaluate.py`: run the benchmark dataset against the decision-tree system.

## MarkItDown Workflow

Install the PDF converter dependency first:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python3 scripts/extract_methods_results_markdown.py
```

By default the script reads PDFs from `data/papers` and writes extracted markdown files to `data/markdown_outputs`.
