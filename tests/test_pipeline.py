import unittest
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from train import prepare_events, chronological_split, make_pipeline, GEO


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.raw = pd.read_csv('data/earthquakes.csv')

    def test_deduplication_and_split(self):
        frame = prepare_events(self.raw)
        self.assertTrue(frame.id.is_unique)
        train, test = chronological_split(frame)
        self.assertFalse(set(train.id) & set(test.id))
        self.assertLess(train.date.max(), test.date.min())

    def test_imputation_uses_training_only(self):
        x = pd.DataFrame({c: [1., 3., np.nan] for c in GEO})
        pipe = make_pipeline(DummyRegressor(), 'geo').fit(x, [3, 4, 5])
        before = pipe.named_steps['preprocess'].named_transformers_['numeric'].statistics_.copy()
        pipe.predict(pd.DataFrame({c: [1e9, np.nan] for c in GEO}))
        np.testing.assert_equal(before, [2., 2., 2.])
        np.testing.assert_equal(before, pipe.named_steps['preprocess'].named_transformers_['numeric'].statistics_)

    def test_unknown_category(self):
        frame = prepare_events(self.raw)
        train, test = chronological_split(frame)
        pipe = make_pipeline(DummyRegressor(), 'catalog').fit(train, train.magnitude)
        test.loc[:, 'continent'] = 'unseen-region'
        self.assertTrue(np.isfinite(pipe.predict(test)).all())

    def test_missing_schema(self):
        with self.assertRaises(ValueError):
            prepare_events(self.raw.drop(columns='magnitude'))

    def test_invalid_target(self):
        self.raw.loc[0, 'magnitude'] = np.nan
        with self.assertRaises(ValueError):
            prepare_events(self.raw)


if __name__ == '__main__':
    unittest.main()
