# Ad Optimization Agent

## Project Overview

This project builds a small, explainable agent that optimizes daily advertising budgets across three channels: Search, Social, and Display.

The agent reads campaign performance data from a CSV file, calculates advertising metrics, recommends a new daily budget for each channel, applies safety guardrails, and compares its results with an equal-split baseline.

The project is a simulation for an Agentic AI in Marketing and Advertising assignment. It does not change real advertising campaigns or use personal customer information.

## Project Goal

The goal is to maximize expected conversions while keeping budget changes stable and reviewable.

The agent uses historical conversion yield as its main performance signal:

```text
Conversion yield = conversions / spend
```

The project evaluates performance using expected conversions, blended cost per acquisition (CPA), and conversion lift compared with an equal-split baseline.

## How the Agent Works

1. Read campaign data from a CSV file.
2. Calculate CTR, CVR, conversion yield, and CPA.
3. Review prior performance for each channel.
4. Recommend the next day's budget.
5. Apply budget guardrails.
6. Log the reason for each budget change.
7. Compare the optimized strategy with an equal-split baseline.

The agent only uses earlier dates when creating a recommendation for a later date, preventing future information from influencing past decisions.

## Guardrails

- Total daily budget: `$300`
- Minimum channel budget: `$60`
- Maximum channel budget: `$180`
- Maximum daily budget change: `20%`
- Every channel keeps a minimum allocation so the agent can continue learning
- Recommendations are for human review and do not modify live campaigns

## Project Files

| File | Purpose |
|---|---|
| `ad_optimization_agent.ipynb` | Google Colab notebook for running the project |
| `ad_optimization_agent.py` | Python implementation of the agent |
| `ad_campaign_data.csv` | 21 days of mock data for three advertising channels |
| `design_document.md` | One-page explanation of the agent design |
| `scaling_note.md` | Cloud deployment, monitoring, and cost-control plan |
| `secrets_setup.md` | Optional API-key and secret-management instructions |
| `presentation_outline.md` | Presentation speaking notes |
| `ad_optimization_agent_presentation.pptx` | 2–3 minute presentation slides |
| `requirements.txt` | Python packages used by the project |

## Requirements

- Python 3.9 or newer
- pandas
- numpy
- matplotlib
- Jupyter Notebook or Google Colab

No API key is required to run the submitted version.

## Running the Project in Google Colab

Google Colab is recommended because it runs Python in the browser.

1. Open [Google Colab](https://colab.research.google.com/).
2. Upload `ad_optimization_agent.ipynb`.
3. Upload `ad_optimization_agent.py` and `ad_campaign_data.csv` into the Colab session.
4. Run the notebook cells from top to bottom.
5. Review the metrics, budget recommendations, decision log, evaluation table, and chart.

## Running the Project Locally

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the Python script:

```bash
python ad_optimization_agent.py
```

The script prints channel performance metrics, final recommended budgets, evaluation results, and sample decision-log entries.

## Example Results

Using the included mock dataset, the agent produced this final-day recommendation:

| Channel | Recommended budget |
|---|---:|
| Search | `$151.05` |
| Social | `$88.95` |
| Display | `$60.00` |
| **Total** | **`$300.00`** |

The simulated evaluation produced:

| Strategy | Expected conversions | Blended CPA |
|---|---:|---:|
| Equal-split baseline | 1,250.0 | `$5.04` |
| Optimized agent | 1,486.6 | `$4.24` |

This represents an estimated `18.9%` conversion lift compared with the equal-split baseline. These results use mock data and do not represent real campaign performance.

## API Keys and Secrets

The current project does not require an API key because the optimization logic uses transparent Python rules.

If an instructor requires an optional LLM version, use `OPENAI_API_KEY` as a protected environment variable through GitHub Codespaces or Google Colab Secrets. Never place an actual key directly in a notebook, Python file, README, or GitHub repository.

The `secrets_setup.md` file explains how to configure a secret safely.

## Limitations

- The campaign data is simulated.
- The agent uses a simple historical conversion-yield heuristic.
- The evaluation estimates conversions rather than measuring live results.
- The project does not connect to Google Ads, Meta Ads, or another advertising platform.
- A human should approve recommendations before any production budget change.

## Possible Future Improvements

- Connect to a real advertising-data API.
- Add confidence intervals and minimum sample-size checks.
- Include audience, creative, location, and device-level data.
- Add an optional LLM explanation layer.
- Run the workflow automatically once per day in a cloud environment.
- Add monitoring alerts and a rollback process.

## Security

Do not commit API keys, passwords, tokens, or `.env` files to GitHub. The `.gitignore` file is included to help prevent accidental secret uploads.
