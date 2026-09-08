# conservation-llm-critical-appraisal

Benchmarking Large Language Models (LLMs) against human experts for critical appraisal of conservation literature using the CEECAT framework.

## Project layout

- `domain_shot/`: prompt builders for tree-guided and question-scoring appraisal methods.
- `sequential_decision_tree/`: sequential decision-tree evaluation system based on CEECAT domain trees.
- `pipeline/`: orchestration layer for running appraisals across models, methods, and papers.
- `scripts/`: command-line entry points for the main workflows.
- `data/`: benchmark data, decision trees, domain questions, and guidance assets.
- `analysis/`: data processing and export utilities.
- `tests/`: unit tests for prompt builders and extractors.

## Main entry points

- `scripts/run_pipeline.py`: run the appraisal pipeline across multiple models and methods, with chunking and resumability.
- `scripts/run_three_methods_multi_model.py`: run all three appraisal methods (sequential, tree-guided, question-scoring) on papers.
- `scripts/export_results.py`: merge per-paper result files into consolidated JSON exports.
- `scripts/pipeline_status.py`: show progress per model and method.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment variables (copy `.env.example` to `.env` and fill in your API keys).

3. Run the pipeline:

```bash
python scripts/run_pipeline.py --dry-run  # preview the plan
python scripts/run_pipeline.py --limit 2   # smoke test with 2 papers
python scripts/run_pipeline.py             # full run
```

## Output

Results are written to `output/<model>/` directories and can be exported to `analysis/appraisals_long.csv` using `analysis/build_dataset.py`.
