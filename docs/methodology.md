# Methodology and model scope

## Distinct experiment records

1. The earlier `original-experiments.ipynb` notebook compares default regressors using a random 80/20 row split, seed 42, median imputation and one-hot encoding before the split. It retains catalog attributes including `sig`, `mmi`, `cdi` and `alert`.
2. The latest `earthquake-analysis-v2.ipynb` notebook uses a Random Forest classifier to fill missing alerts, IQR clipping (winsorization), ordinal encoding, Random Forest and Gradient Boosting regressors, and grid-search tuning. The report documents this academic work; its IQR discussion describes filtering, while the supplied v2 code clips values. Saved outputs are historical.
3. `train.py` is the reproducible evaluation: deterministic event-ID deduplication, a chronological holdout, train-only transformations and a median baseline. It does not apply IQR filtering or hyperparameter search.

## Data audit

The supplied CSV contains 1,137 records, 43 columns, 602 unique IDs, 337 exact duplicate rows and 535 repeated-ID rows beyond the first occurrence. Repeating the notebook's row split yields 134 shared event IDs between training and test sets.

The training script orders revisions by numeric `updated`, retaining the last record per ID. Ties retain the last input occurrence. Events are sorted by `date`. The cutoff is the date at the 80% index; all events at that timestamp stay together on the test side. The resulting split has 481 training and 121 test events.

This separates identical IDs, not necessarily physical earthquakes reported under different network IDs. The CSV's catalog revisions are not reconstructed as they existed at each historical cutoff.

## Features and leakage

The primary comparison uses longitude, latitude and depth. All describe an observed event, not an earthquake before occurrence.

The diagnostic comparison uses 13 catalog inputs from the earlier experiment, including significance, intensity and alert information. USGS defines significance (`sig`) using factors that include magnitude. Such attributes can leak target-related information. Lower diagnostic errors should not be advertised as operational forecasting performance.

Both historical notebooks perform preprocessing before the final magnitude train/test split. In v2, the alert classifier, IQR limits and ordinal encoders are fitted before that split. The maintained pipeline instead fits numerical medians and categorical encoders on training events only. Unknown test categories are handled without fitting again on the test set. See [scikit-learn guidance](https://scikit-learn.org/stable/common_pitfalls.html).

## Models and metrics

All models use fixed settings, with no tuning on the held-out events. Random Forest uses 100 trees; both ensembles use seed 42. The median baseline predicts the training target median. MAE and RMSE use magnitude units; MSE uses squared units. R² may be negative when a model performs worse than a constant prediction at the test mean.

One chronological holdout does not establish broad generalization. Future work should use rolling-origin evaluation, spatial/group holdouts and an independent later dataset, with all model-selection decisions inside training folds.

## Outliers and scope

The maintained pipeline does not remove large events using target-based IQR filtering. Excluding extreme magnitudes would change the evaluated population and could remove cases most important to study. The historical IQR experiments remain academic variants, not an unqualified preprocessing recommendation.

This project does not supply event-occurrence forecasts, uncertainty calibration, seismic-hazard estimates or operational warnings.
