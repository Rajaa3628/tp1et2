import numpy as np
import pandas as pd
from app.preprocessing import split_and_scale


def test_split_reproducibility():
    """Verifie l'invariance du partitionnement via la graine aleatoire."""
    df = pd.DataFrame({
        "feature1": range(100),
        "feature2": range(100),
        "pm25": range(100),
    })

    config = {
        "data": {"target_column": "pm25", "test_size": 0.2},
        "project": {"random_seed": 42},
        "preprocessing": {"scale_features": True},
    }

    X_train1, X_test1, _, _, _ = split_and_scale(df, config)
    X_train2, X_test2, _, _, _ = split_and_scale(df, config)

    np.testing.assert_array_equal(X_train1, X_train2)
    np.testing.assert_array_equal(X_test1, X_test2)
