"""Module de pretraitement des donnees."""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, Any


def clean_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    df_clean = df.copy()
    handle_missing = config["preprocessing"]["handle_missing"]

    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if handle_missing == "median":
                median_value = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_value)

    threshold = config["preprocessing"]["outlier_threshold"]
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col != config["data"]["target_column"]:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            df_clean[col] = df_clean[col].clip(lower, upper)

    return df_clean


def split_and_scale(
    df: pd.DataFrame, config: Dict[str, Any]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """Partitionne les données et normalise les features si demandé."""
    target_col = config["data"]["target_column"]
    test_size = config["data"]["test_size"]
    random_seed = config["project"]["random_seed"]
    scale_features = config["preprocessing"].get("scale_features", False)

    X = df.drop(columns=[target_col])
    y = df[target_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_seed,
    )

    scaler = StandardScaler()

    if scale_features:
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    else:
        X_train = X_train.values
        X_test = X_test.values

    return X_train, X_test, y_train, y_test, scaler
