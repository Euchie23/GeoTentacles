import numpy as np
import pandas as pd


def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())


def compute_ecopulse_index(
    df,
    pollution_col="concentration",
    size_col="Mantle_length_mm",
    tissue_col="Tissue",
    weights=None
):
    df = df.copy()

    if weights is None:
        weights = {
            "pollution": 0.5,
            "size": 0.3,
            "tissue": 0.2
        }

    # Scale pollution (higher = worse)
    df["pollution_score"] = min_max_scale(df[pollution_col])

    # Scale size (larger = healthier)
    df["size_score"] = min_max_scale(df[size_col])

    # Tissue exposure risk (simple, transparent)
    tissue_risk = {
        "muscle": 0.5,
        "digestive": 1.0,
        "gill": 0.8
    }
    df["tissue_score"] = df[tissue_col].map(tissue_risk).fillna(0.6)

    # Composite index (higher = healthier)
    df["EcoPulse"] = (
        (1 - df["pollution_score"]) * weights["pollution"] +
        df["size_score"] * weights["size"] +
        (1 - df["tissue_score"]) * weights["tissue"]
    )

    return df
