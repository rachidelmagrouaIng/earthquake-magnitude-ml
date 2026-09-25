# Earthquake Magnitude Estimation

**From exploratory analysis to reproducible model evaluation on earthquake catalog data.**

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-in%20development-0F766E)
[![Validate ML pipeline](https://github.com/rachidelmagrouaIng/earthquake-magnitude-ml/actions/workflows/tests.yml/badge.svg)](https://github.com/rachidelmagrouaIng/earthquake-magnitude-ml/actions/workflows/tests.yml)

**Maintained by Rachid EL MAGROUA · Network & Cybersecurity Engineer**

I am developing this academic project into a documented ML portfolio repository. The current version includes the experiments, dataset, report, a reproducible evaluation script and automated checks. See the [development roadmap](ROADMAP.md) for planned improvements.

**Recruiters:** start with the [project brief](docs/project-brief.md), inspect the [latest notebook](notebooks/earthquake-analysis-v2.ipynb), or [contact me on LinkedIn](https://www.linkedin.com/in/rachid-el-magroua/).

[Français](README.fr.md) · [Notebook v2](notebooks/earthquake-analysis-v2.ipynb) · [Project report](reports/project-report-fr.pdf) · [Methodology](docs/methodology.md) · [Results](docs/results.md)

## Project overview

I worked on this academic machine-learning project with Anas DARRAZ, Ilyas MAJDOUBI and Nabil EL HILALI, under the supervision of Asmae BENTALB during 2024/2025.

Our objective was to estimate earthquake magnitude from recorded event attributes and compare Linear Regression, Random Forest and Gradient Boosting. The repository includes the original experiments and a separate, reproducible evaluation with event deduplication and a chronological holdout.

**Scope:** retrospective magnitude regression. The inputs describe recorded events; the project does not forecast when or where a future earthquake will occur and is not an early-warning system.

## Engineering highlights

- Explore numerical distributions, category frequencies and feature relationships.
- Compare regression models against a median baseline.
- Audit repeated event IDs and target-related predictors.
- Fit imputers and encoders on training data through scikit-learn pipelines.
- Record dataset hashes, runtime versions, predictions and evaluation metrics.
- Test event separation, missing-value handling and unseen categories.

## Latest reproducible evaluation

The 1,137-row dataset contains 602 unique event IDs. The pipeline keeps one revision per ID, then uses 481 earlier events for training and 121 later events for testing. No event ID appears in both sets.

Location/depth-only features: `longitude`, `latitude`, `depth`.

| Model | MAE ↓ | RMSE ↓ | R² ↑ |
| --- | ---: | ---: | ---: |
| Median baseline | 1.418 | 1.570 | -2.848 |
| Linear Regression | 0.528 | 0.659 | 0.323 |
| Random Forest | 0.427 | 0.536 | 0.552 |
| Gradient Boosting | **0.401** | **0.517** | **0.582** |

These are results on one chronological holdout, not a claim of universal superiority. Even location and depth are observed event attributes, so this remains retrospective estimation.

![Model comparison on the chronological holdout](results/model-comparison.png)

The second panel deliberately includes catalog attributes such as `sig`, `mmi` and `alert`. It is a leakage diagnostic, not a deployable model comparison. USGS describes `sig` as partly determined by magnitude. Its use to estimate magnitude can therefore expose information about the target.

## Quick start

Use Python 3.12. From the repository root:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train.py --output results-local
python -m unittest discover -s tests -v
```

The training command produces metrics, per-event predictions, run metadata and a comparison chart. It does not serialize model objects. Run it without `--output` only if you intend to replace the tracked results.

To explore the v2 notebook, open `notebooks/earthquake-analysis-v2.ipynb` in VS Code or Jupyter with the environment above. It accepts either the repository root or `notebooks/` as the working directory. Install Jupyter separately if your editor does not provide it. Full grid search runs hundreds of fits and can take time. Saved notebook outputs are historical and have not been overwritten with the chronological evaluation.

The earlier notebook is retained as `notebooks/original-experiments.ipynb`; run it with `notebooks/` as the working directory.

## Repository guide

| Path | Contents |
| --- | --- |
| `train.py` | Validated schema, event deduplication, chronological split and model comparison |
| `data/earthquakes.csv` | Dataset supplied with the academic project |
| `notebooks/earthquake-analysis-v2.ipynb` | Latest academic notebook: EDA, IQR clipping, alert imputation and tuned ensembles |
| `notebooks/original-experiments.ipynb` | Earlier experiment version, retained for reference |
| `reports/project-report-fr.pdf` | Original French report, including IQR filtering and tuning discussion |
| `docs/methodology.md` | Evaluation choices and limits |
| `docs/results.md` | Separate historical and chronological evaluation results |
| `docs/project-brief.md` | Short overview of skills, evidence and project scope |
| `ROADMAP.md` | Completed work and planned improvements |
| `CHANGELOG.md` | Dated record of repository changes |
| `results/` | Reproducible run outputs |
| `tests/` | Five checks of the evaluation pipeline |
| `.github/workflows/tests.yml` | Tests and training smoke run on GitHub Actions |

## What the review changed

The original random split places 134 event IDs in both train and test sets. Preprocessing also uses the full dataset before splitting. Those choices, together with target-related catalog fields, limit interpretation of the original low errors.

The reproducible pipeline addresses repeated IDs and preprocessing leakage and provides a restricted feature comparison. It does not reconstruct historical data availability: retained catalog revisions may include later updates. Different catalog IDs may also represent the same physical event.

See [methodology](docs/methodology.md) for details. The earlier notebook, v2 notebook/report and chronological evaluation represent separate experiments; their scores should not be combined as if produced by one pipeline.

## Authors

- Rachid EL MAGROUA — [GitHub](https://github.com/rachidelmagrouaIng)
- Anas DARRAZ
- Ilyas MAJDOUBI
- Nabil EL HILALI

Academic supervisor: Asmae BENTALB.

## References

- [USGS ComCat field definitions](https://earthquake.usgs.gov/data/comcat/)
- [scikit-learn: avoiding data leakage](https://scikit-learn.org/stable/common_pitfalls.html)

Dataset provenance and licensing notes are in [data/README.md](data/README.md).
