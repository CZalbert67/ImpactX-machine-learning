"""Synthetic training dataset for the first ImpactX prototype.

The generated samples are intentionally illustrative. They are not clinical or automotive
validation data and must not be treated as production thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from impactx_ml.domain import FEATURE_NAMES, Severity


@dataclass(frozen=True, slots=True)
class Distribution:
    mean: float
    std: float
    minimum: float
    maximum: float


CLASS_CONFIG: dict[Severity, dict[str, Distribution]] = {
    Severity.NO_COLLISION: {
        "g_force_peak": Distribution(1.2, 0.7, 0.0, 4.5),
        "heart_rate_bpm": Distribution(78, 16, 42, 150),
        "impact_duration_ms": Distribution(35, 24, 0, 140),
        "speed_delta_kmh": Distribution(1.5, 2.0, 0, 8),
        "post_impact_inactivity_seconds": Distribution(1, 2, 0, 8),
    },
    Severity.MILD: {
        "g_force_peak": Distribution(4.2, 1.3, 1.8, 8.5),
        "heart_rate_bpm": Distribution(92, 22, 45, 170),
        "impact_duration_ms": Distribution(110, 55, 20, 320),
        "speed_delta_kmh": Distribution(9, 6, 0, 28),
        "post_impact_inactivity_seconds": Distribution(4, 5, 0, 22),
    },
    Severity.MODERATE: {
        "g_force_peak": Distribution(7.8, 2.0, 3.5, 13.5),
        "heart_rate_bpm": Distribution(116, 28, 45, 195),
        "impact_duration_ms": Distribution(245, 105, 50, 650),
        "speed_delta_kmh": Distribution(28, 13, 4, 65),
        "post_impact_inactivity_seconds": Distribution(18, 17, 0, 70),
    },
    Severity.SEVERE: {
        "g_force_peak": Distribution(13.5, 3.0, 7, 22),
        "heart_rate_bpm": Distribution(145, 34, 38, 225),
        "impact_duration_ms": Distribution(490, 180, 100, 1050),
        "speed_delta_kmh": Distribution(55, 21, 12, 110),
        "post_impact_inactivity_seconds": Distribution(62, 45, 4, 190),
    },
    Severity.CRITICAL: {
        "g_force_peak": Distribution(20.5, 4.0, 11, 30),
        "heart_rate_bpm": Distribution(168, 42, 30, 240),
        "impact_duration_ms": Distribution(820, 260, 180, 1600),
        "speed_delta_kmh": Distribution(88, 28, 24, 160),
        "post_impact_inactivity_seconds": Distribution(150, 78, 20, 300),
    },
}

CLASS_PROBABILITIES = {
    Severity.NO_COLLISION: 0.44,
    Severity.MILD: 0.23,
    Severity.MODERATE: 0.16,
    Severity.SEVERE: 0.11,
    Severity.CRITICAL: 0.06,
}


def _sample_distribution(
    rng: np.random.Generator, distribution: Distribution, size: int
) -> np.ndarray:
    values = rng.normal(distribution.mean, distribution.std, size=size)
    return np.clip(values, distribution.minimum, distribution.maximum)


def generate_synthetic_dataset(
    n_samples: int = 15_000,
    random_state: int = 42,
) -> pd.DataFrame:
    """Create a reproducible, overlapping synthetic collision dataset."""
    if n_samples < 500:
        raise ValueError("n_samples must be at least 500")

    rng = np.random.default_rng(random_state)
    labels = list(CLASS_PROBABILITIES)
    probabilities = list(CLASS_PROBABILITIES.values())
    sampled_labels = rng.choice(labels, size=n_samples, p=probabilities)

    rows: list[dict[str, float | str]] = []
    for severity in labels:
        mask = sampled_labels == severity
        count = int(mask.sum())
        if count == 0:
            continue
        config = CLASS_CONFIG[severity]
        generated = {
            feature: _sample_distribution(rng, config[feature], count)
            for feature in FEATURE_NAMES
        }

        # A small number of abnormal low-heart-rate critical events makes the dataset less trivial.
        if severity in {Severity.SEVERE, Severity.CRITICAL}:
            low_rate_mask = rng.random(count) < (0.08 if severity == Severity.SEVERE else 0.18)
            low_rates = rng.normal(42, 8, size=count)
            generated["heart_rate_bpm"][low_rate_mask] = np.clip(
                low_rates[low_rate_mask], 25, 65
            )

        for index in range(count):
            row = {feature: float(generated[feature][index]) for feature in FEATURE_NAMES}
            row["severity"] = severity.value
            rows.append(row)

    frame = pd.DataFrame(rows)
    integer_columns = [
        "heart_rate_bpm",
        "impact_duration_ms",
        "post_impact_inactivity_seconds",
    ]
    frame[integer_columns] = frame[integer_columns].round().astype(int)
    return frame.sample(frac=1, random_state=random_state).reset_index(drop=True)
