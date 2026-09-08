"""Build the long-format analysis table from per-paper appraisal JSONs.

One row per (paper x domain x model x method). Columns:

    paper_id, domain, model, method, judgement, score_0_10, applicable

- judgement: normalised Low / Medium / High / Not applicable (sequential and
  tree_guided). Empty for question_scoring (which is numeric) and for any
  assessment that errored or lacked the expected field.
- score_0_10: integer 0-10 for question_scoring only; empty otherwise.
  No thresholding is applied -- categorisation is left to downstream analysis.
  Note: score 0 is overloaded (it means both "no identifiable risk" and, by
  prompt rule, "Not applicable"), so do NOT categorise from the score alone --
  use `applicable` to separate the two.
- applicable: "yes" / "no" / "" (unknown). For question_scoring this is derived
  from question_answers (a domain where every answer is "Not applicable" is
  "no"); for categorical methods it comes from the judgement.

Expert ground truth is NOT joined here; that is added downstream in R.

Usage:
    python analysis/build_dataset.py
    python analysis/build_dataset.py --out analysis/appraisals_long.csv
"""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "output"

MODELS = ["claude-opus-5", "glm-5.2", "deepseek-v4-pro", "gpt-5.6-sol"]
METHODS = ["sequential", "tree_guided", "question_scoring"]
DOMAINS = [str(i) for i in range(1, 8)]

# Labels that did not map cleanly, collected for review rather than dropped.
unmapped = []

def _norm_token(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def norm_sequential(result) -> tuple[str, bool]:
    """Map a sequential `result` string to (judgement, unusable)."""
    if not isinstance(result, str):
        return "", True
    t = _norm_token(result)
    if t.startswith("error"):
        return "", True
    if t.startswith("not applicable"):
        return "Not applicable", False
    if t.startswith("low"):
        return "Low", False
    if t.startswith("high"):
        return "High", False
    if t.startswith("med"):  # MED, MEDIUM RISK, ...
        return "Medium", False
    unmapped.append(("sequential", result))
    return "", True


def norm_tree_guided(judgement) -> tuple[str, bool]:
    """Map a tree_guided `final_risk_judgement` to (judgement, unusable)."""
    if judgement is None:
        return "", True
    if not isinstance(judgement, str):
        return "", True
    t = _norm_token(judgement)
    if t.startswith("error"):
        return "", True
    if t.startswith("not applicable"):
        return "Not applicable", False
    if t.startswith("low"):
        return "Low", False
    if t.startswith("high"):
        return "High", False
    if t.startswith("medium") or t.startswith("med"):
        return "Medium", False
    unmapped.append(("tree_guided", judgement))
    return "", True


def parse_file(path: Path, model: str, method: str, paper_id: int) -> list[dict]:
    """Return one row per domain for a single per-paper file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return [_row(paper_id, None, model, method, "", None, "")]

    rows = []
    for domain in DOMAINS:
        entry = data.get(domain)
        judgement, score, applicable = "", None, ""

        if not isinstance(entry, dict):
            pass
        elif method == "sequential":
            judgement, _ = norm_sequential(entry.get("result"))
            applicable = _applicable_from_judgement(judgement)
        elif method == "tree_guided":
            parsed = entry.get("parsed_response")
            if isinstance(parsed, dict):
                judgement, _ = norm_tree_guided(parsed.get("final_risk_judgement"))
                applicable = _applicable_from_judgement(judgement)
        elif method == "question_scoring":
            parsed = entry.get("parsed_response")
            if isinstance(parsed, dict):
                raw = parsed.get("risk_of_bias_score_0_to_10")
                if isinstance(raw, int) and not isinstance(raw, bool):
                    score = raw
                applicable = _applicable_from_answers(parsed.get("question_answers"))

        rows.append(_row(paper_id, int(domain), model, method, judgement, score, applicable))
    return rows


def _applicable_from_judgement(judgement: str) -> str:
    """For categorical methods, applicability comes from the judgement itself."""
    if judgement == "Not applicable":
        return "no"
    if judgement in ("Low", "Medium", "High"):
        return "yes"
    return ""


def _applicable_from_answers(question_answers) -> str:
    """For question_scoring, a domain is Not applicable when every answer is
    'Not applicable' (score is then 0 by rule, so the score alone is ambiguous).
    """
    if not isinstance(question_answers, dict) or not question_answers:
        return ""
    all_na = all(str(v).strip().lower().startswith("not applicable") for v in question_answers.values())
    return "no" if all_na else "yes"


def _row(paper_id, domain, model, method, judgement, score, applicable) -> dict:
    return {
        "paper_id": paper_id,
        "domain": domain,
        "model": model,
        "method": method,
        "judgement": judgement,
        "score_0_10": score,
        "applicable": applicable,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(REPO_ROOT / "analysis" / "appraisals_long.csv"))
    args = parser.parse_args()

    rows = []
    files = 0
    for model in MODELS:
        for method in METHODS:
            for path in sorted((OUTPUT / model / method).glob("*.json")):
                stem = path.stem
                if not stem.isdigit():
                    continue
                rows.extend(parse_file(path, model, method, int(stem)))
                files += 1

    df = pd.DataFrame(rows)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    # ---- verification report ----
    print(f"Wrote {len(df)} rows from {files} files -> {out_path}\n")
    print("rows per model x method:")
    print(df.groupby(["model", "method"]).size().to_string())
    print("\njudgement distribution (categorical methods):")
    print(df[df.method != "question_scoring"]["judgement"].value_counts(dropna=False).to_string())
    print("\nscore_0_10 present:", df["score_0_10"].notna().sum(),
          " range:", df["score_0_10"].min(), "-", df["score_0_10"].max())
    print("\napplicable counts per method:")
    print(df.groupby(["method", "applicable"], dropna=False).size().to_string())
    # the score-0 ambiguity check: how many score==0 rows are applicable vs not
    qs0 = df[(df.method == "question_scoring") & (df.score_0_10 == 0)]
    print("\nquestion_scoring score==0 rows by applicable:")
    print(qs0["applicable"].value_counts(dropna=False).to_string())
    if unmapped:
        from collections import Counter
        print(f"\nUNMAPPED labels ({len(unmapped)}):")
        for (meth, label), n in Counter(unmapped).most_common():
            print(f"  {n:4d}  [{meth}] {label!r}")
    else:
        print("\nNo unmapped labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
