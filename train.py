"""Retrospective magnitude regression with event-disjoint chronological evaluation."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

GEO = ['longitude', 'latitude', 'depth']
NUMERIC = GEO + ['sig', 'nst', 'rms', 'dmin', 'mmi', 'cdi']
CATEGORICAL = ['alert', 'status', 'magType', 'continent']


def prepare_events(raw):
    required = ['id', 'date', 'magnitude'] + NUMERIC + CATEGORICAL
    missing = sorted(set(required) - set(raw.columns))
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(missing))
    frame = raw.copy()
    if frame.id.isna().any() or frame.id.astype(str).str.strip().eq('').any():
        raise ValueError('Every event must have an ID')
    frame['date'] = pd.to_datetime(frame.date, utc=True, errors='raise')
    if frame.date.isna().any():
        raise ValueError('Event dates cannot be missing')
    frame['magnitude'] = pd.to_numeric(frame.magnitude, errors='raise')
    if not np.isfinite(frame.magnitude).all():
        raise ValueError('Target must be finite and non-missing')
    for col in NUMERIC:
        frame[col] = pd.to_numeric(frame[col], errors='raise').replace([np.inf, -np.inf], np.nan)
    # Preserve a deterministic latest recorded revision, when available.
    if 'updated' in frame:
        frame['_updated'] = pd.to_numeric(frame.updated, errors='coerce').fillna(-1)
        frame = frame.sort_values('_updated', kind='stable').drop(columns='_updated')
    frame = frame.drop_duplicates('id', keep='last').sort_values('date', kind='stable')
    return frame.reset_index(drop=True)


def chronological_split(frame):
    if len(frame) < 10:
        raise ValueError('At least 10 unique events are required')
    cutoff = frame.date.iloc[int(len(frame) * 0.8)]
    train = frame.loc[frame.date < cutoff].copy()
    test = frame.loc[frame.date >= cutoff].copy()
    if len(train) < 5 or len(test) < 2:
        raise ValueError('Insufficient events on either side of the time cutoff')
    if set(train.id) & set(test.id):
        raise ValueError('Event IDs overlap across the split')
    return train, test


def make_pipeline(model, features='geo'):
    nums = GEO if features == 'geo' else NUMERIC
    transforms = [('numeric', SimpleImputer(strategy='median', keep_empty_features=True), nums)]
    if features == 'catalog':
        transforms.append(('categorical', Pipeline([
            ('impute', SimpleImputer(strategy='constant', fill_value='unknown')),
            ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
        ]), CATEGORICAL))
    return Pipeline([('preprocess', ColumnTransformer(transforms)), ('model', model)])


def run(csv_path, output):
    raw = pd.read_csv(csv_path)
    frame = prepare_events(raw)
    train, test = chronological_split(frame)
    models = {
        'Median baseline': DummyRegressor(strategy='median'),
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=1),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    }
    rows, predictions = [], []
    for features in ['geo', 'catalog']:
        for name, model in models.items():
            from sklearn.base import clone
            pipe = make_pipeline(clone(model), features)
            pipe.fit(train, train.magnitude)
            pred = pipe.predict(test)
            mse = mean_squared_error(test.magnitude, pred)
            rows.append({'features': features, 'model': name,
                         'mae': mean_absolute_error(test.magnitude, pred),
                         'mse': mse, 'rmse': float(np.sqrt(mse)),
                         'r2': r2_score(test.magnitude, pred)})
            predictions.extend({'id': eid, 'features': features, 'model': name,
                                'actual': actual, 'predicted': value}
                               for eid, actual, value in zip(test.id, test.magnitude, pred))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    scores = pd.DataFrame(rows)
    scores.to_csv(output / 'metrics.csv', index=False)
    pd.DataFrame(predictions).to_csv(output / 'predictions.csv', index=False)
    metadata = {
        'task': 'Retrospective magnitude estimation; not future-event forecasting',
        'dataset_sha256': hashlib.sha256(Path(csv_path).read_bytes()).hexdigest(),
        'rows_raw': len(raw), 'unique_events': len(frame),
        'duplicate_id_rows_removed': len(raw) - len(frame),
        'train_rows': len(train), 'test_rows': len(test),
        'train_end': str(train.date.max()), 'test_start': str(test.date.min()),
        'shared_event_ids': len(set(train.id) & set(test.id)),
        'seed': 42, 'python': platform.python_version(),
        'pandas': pd.__version__, 'numpy': np.__version__, 'scikit_learn': sklearn.__version__,
        'geo_features': GEO, 'catalog_features': NUMERIC + CATEGORICAL,
        'catalog_warning': 'Diagnostic only: includes target-related and post-event fields',
    }
    (output / 'run.json').write_text(json.dumps(metadata, indent=2) + '\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7))
    for ax, features, title in zip(axes, ['geo', 'catalog'], ['Location + depth', 'Catalog attributes (leakage diagnostic)']):
        part = scores.loc[scores.features == features]
        ax.barh(part.model, part.mae, color='#176b87' if features == 'geo' else '#a45f29')
        ax.invert_yaxis()
        ax.set_title(title, fontsize=11)
        ax.set_xlabel('MAE (magnitude units; lower is better)')
        for i, v in enumerate(part.mae):
            ax.text(v, i, f' {v:.3f}', va='center', fontsize=9)
        ax.set_xlim(0, max(part.mae) * 1.22)
    fig.suptitle('Chronological holdout after event-ID deduplication', fontsize=13)
    fig.tight_layout()
    fig.savefig(output / 'model-comparison.png', dpi=170)
    plt.close(fig)
    print(scores.to_string(index=False))
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('data/earthquakes.csv'))
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    run(args.data, args.output)
