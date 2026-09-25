# Results and validation

## Earlier notebook outputs

The following values are recorded in the supplied notebook, not newly generated holdout scores:

| Model | MAE | MSE |
| --- | ---: | ---: |
| Linear Regression | 0.193194 | 0.067744 |
| Random Forest | 0.037838 | 0.007298 |
| Gradient Boosting | 0.068551 | 0.012425 |

These use a random row split and include repeated event IDs across partitions, full-data preprocessing and target-related features. They must be interpreted with those limitations.

## Latest academic notebook (v2)

Historical saved outputs in `notebooks/earthquake-analysis-v2.ipynb`:

| Model / stage | MAE | MSE | R² |
| --- | ---: | ---: | ---: |
| Random Forest, before tuning | 0.028051 | 0.004458 | 0.9959 |
| Gradient Boosting, before tuning | 0.051924 | 0.007402 | 0.9931 |
| Random Forest, after tuning | 0.028051 | 0.004458 | 0.9959 |
| Gradient Boosting, after tuning | 0.026508 | 0.003424 | 0.9968 |

The high scores are from a random row split with full-data preprocessing and target-related inputs. They are **not forecasting accuracy** and are not comparable to the chronological experiment as a controlled before/after test. The v2 alert classifier has no fixed random seed. We fixed a syntax typo in its metric print statement and adjusted the data path; saved outputs were preserved. Full grid search has not been rerun during this repository update.

## Academic report

The report discusses a separate pipeline with IQR filtering, alert imputation and hyperparameter tuning. Its printed page 25 records optimized Random Forest MAE approximately 0.028051 / MSE 0.004458, and Gradient Boosting MAE approximately 0.026508 / MSE 0.003424. These printed values agree, to the displayed precision, with the saved v2 notebook outputs; the tuning run has not been independently reproduced during this update. The plotted bars on that page do not clearly match all printed values, so the report is retained as historical documentation rather than treated as the current benchmark.

## Reproducible evaluation

Run `python train.py --output results-local` to reproduce the maintained experiment. Exact metrics are in [metrics.csv](../results/metrics.csv), predictions in [predictions.csv](../results/predictions.csv), and split boundaries, seed, runtime and dataset checksum in [run.json](../results/run.json).

Location/depth-only Gradient Boosting has the lowest MAE on this particular holdout (0.401102). The catalog-feature Random Forest gives MAE 0.116758, but that feature set deliberately retains target-related information and is diagnostic only.

Different splits, event handling and input sets mean these scores cannot be interpreted as a controlled before/after improvement over the original notebook.

## Verification performed

- Training completed on the included CSV for all eight model/feature combinations.
- Five tests passed: event separation, train-only imputation, unseen category handling, missing-schema rejection and invalid-target rejection.
- Dataset checksum and rerun metrics were compared with the recovered project artifacts.
- Saved comparison chart was visually inspected.

Both notebooks were syntax-checked. Their historical tuning experiments were not rerun. The chronological pipeline and its five tests were run locally during the 2026-09-25 repository update. Check the live Actions badge for remote CI status.
