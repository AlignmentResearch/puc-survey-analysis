"""Generate the committed, de-identified dataset from the raw survey export.

Reads the raw Google Forms export (which contains real names + emails) and writes
two files:

  - participant_map.csv   alias -> name/email. Contains PII. GITIGNORED. Keep this
                          locally so you can re-hydrate real names when needed.
  - responses_anon.csv    the same responses with `Name` replaced by an alias
                          (P1, P2, ...) and `Email` removed. Safe to commit.

Aliases are assigned in submission order (by Timestamp) so re-running this script
reproduces the exact same mapping.

Run:  python anonymize.py
"""

from pathlib import Path

import pandas as pd

RAW_XLSX = "PUC Risk Estimation (Responses).xlsx"
MAP_CSV = "participant_map.csv"
ANON_CSV = "responses_anon.csv"


def load_and_filter(path: str) -> pd.DataFrame:
    """Load the raw export and apply the same row filters the analysis uses:
    keep rows with a Name and at least one free-text explanation."""
    df = pd.read_excel(path)
    df = df[df["Name"].notna()]
    qual = [c for c in df.columns if "explain" in c.lower()]
    df = df[df[qual].notna().any(axis=1)]
    return df.sort_values("Timestamp").reset_index(drop=True)


def main() -> None:
    if not Path(RAW_XLSX).exists():
        raise SystemExit(
            f"Raw export '{RAW_XLSX}' not found. This file holds PII and is "
            "gitignored; obtain it from the survey owner before running."
        )

    df = load_and_filter(RAW_XLSX)
    aliases = [f"P{i + 1}" for i in range(len(df))]

    # Identity mapping (PII) — kept out of git.
    mapping = pd.DataFrame(
        {"alias": aliases, "name": df["Name"].values, "email": df["Email"].values}
    )
    mapping.to_csv(MAP_CSV, index=False)

    # De-identified dataset — safe to commit.
    anon = df.copy()
    # Flag data-quality corrections by alias instead of by name (one respondent
    # answered the Q5 ranking on a reversed scale; the notebook flips it).
    anon["q5_reversed"] = anon["Name"].str.contains("Rick", na=False).values
    anon["Name"] = aliases
    anon = anon.drop(columns=["Email"])
    anon.to_csv(ANON_CSV, index=False)

    print(f"Wrote {MAP_CSV} ({len(mapping)} participants) [gitignored]")
    print(f"Wrote {ANON_CSV} ({len(anon)} rows, {anon.shape[1]} cols) [committed]")


if __name__ == "__main__":
    main()
