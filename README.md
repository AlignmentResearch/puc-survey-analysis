# PUC Survey Analysis

Analysis of an expert elicitation survey on the marginal risk that AI persuasion
poses to human control (PUC = persuasion undermining control). Participants rated
five scenarios across realism, persuasion effect, frequency, and impact, then
ranked and contextualized the scenarios.

## De-identification

The committed data is de-identified. Real names and emails never enter git.

- `responses_anon.csv` — committed. The `Name` column holds aliases (`P1`, `P2`, ...);
  emails are removed.
- `participant_map.csv` — **gitignored**. Maps each alias to the real name/email.
- `PUC Risk Estimation (Responses).xlsx` — **gitignored**. The raw survey export.

To regenerate the de-identified data from the raw export:

```bash
python anonymize.py
```

Aliases are assigned in submission order, so the mapping is reproducible.

### Seeing real names locally

`analysis.ipynb` has a `USE_NAMES` flag near the top. When `True` **and**
`participant_map.csv` is present, plots and tables show real names; otherwise they
fall back to aliases. Anyone cloning the repo (who therefore lacks the map) sees
aliases automatically.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then open `analysis.ipynb`. If you only have the anonymized CSV, it runs as-is; if
you also have the raw export, run `python anonymize.py` first.
