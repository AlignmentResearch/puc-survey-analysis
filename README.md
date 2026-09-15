# PUC Survey Analysis

Analysis of an expert elicitation survey on the marginal risk that AI persuasion
poses to human control (PUC = persuasion undermining control). Participants rated
five scenarios across realism, persuasion effect, frequency, and impact, then
ranked and contextualized the scenarios.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then open `analysis.ipynb`. If you only have the anonymized CSV, it runs as-is; if
you also have the raw export, run `python anonymize.py` first.
