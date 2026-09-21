# Earthquake Magnitude Estimation

**Comparing regression models on recorded earthquake data, with reproducible evaluation and an explicit review of data leakage.**

[Français](README.fr.md) · [Notebook](notebooks/original-experiments.ipynb) · [Project report](reports/project-report-fr.pdf) · [Methodology](docs/methodology.md) · [Results](docs/results.md)

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

To explore the original notebook, use a Jupyter-compatible editor with the environment above and set the notebook working directory to `notebooks/`. Install Jupyter separately if your editor does not provide it. Saved notebook outputs are historical and have not been overwritten with the new evaluation.

## Repository guide

| Path | Contents |
| --- | --- |
| `train.py` | Validated schema, event deduplication, chronological split and model comparison |
| `data/earthquakes.csv` | Dataset supplied with the academic project |
| `notebooks/original-experiments.ipynb` | Original code and saved outputs, with the dataset path adjusted |
| `reports/project-report-fr.pdf` | Original French report, including IQR filtering and tuning discussion |
| `docs/methodology.md` | Evaluation choices and limits |
| `docs/results.md` | Separate original, report and rerun results |
| `results/` | Reproducible run outputs |
| `tests/` | Five checks of the evaluation pipeline |
| `.github/workflows/tests.yml` | Tests and training smoke run on GitHub Actions |

## What the review changed

The original random split places 134 event IDs in both train and test sets. Preprocessing also uses the full dataset before splitting. Those choices, together with target-related catalog fields, limit interpretation of the original low errors.

The reproducible pipeline addresses repeated IDs and preprocessing leakage and provides a restricted feature comparison. It does not reconstruct historical data availability: retained catalog revisions may include later updates. Different catalog IDs may also represent the same physical event.

See [methodology](docs/methodology.md) for details. The report and original notebook describe different experiment variants; their scores should not be combined as if produced by one pipeline.

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
