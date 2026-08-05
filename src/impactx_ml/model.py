"""Training and persistence utilities for the ImpactX collision classifier."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from impactx_ml.dataset import generate_synthetic_dataset
from impactx_ml.domain import FEATURE_NAMES, Severity

MODEL_VERSION = "impactx-collision-rf-v1"


@dataclass(frozen=True, slots=True)
class TrainingSummary:
    model_version: str
    artifact_path: str
    samples: int
    accuracy: float
    trained_at_utc: str
    classification_report: dict[str, Any]
    confusion_matrix: list[list[int]]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_model_path() -> Path:
    configured = os.getenv("IMPACTX_MODEL_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return project_root() / "artifacts" / "impactx_collision_model.joblib"


def default_metadata_path() -> Path:
    return default_model_path().with_suffix(".metadata.json")


def train_model(
    artifact_path: Path | None = None,
    metadata_path: Path | None = None,
    n_samples: int = 15_000,
    random_state: int = 42,
    n_estimators: int = 260,
) -> TrainingSummary:
    """Generate demo data, train a Random Forest, evaluate it, and persist the bundle."""
    artifact_path = artifact_path or default_model_path()
    metadata_path = metadata_path or artifact_path.with_suffix(".metadata.json")
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    dataset = generate_synthetic_dataset(n_samples=n_samples, random_state=random_state)
    x = dataset[FEATURE_NAMES]
    y = dataset["severity"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.22,
        random_state=random_state,
        stratify=y,
    )

    classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=14,
        min_samples_leaf=3,
        class_weight="balanced_subsample",
        n_jobs=-1,
        random_state=random_state,
    )
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(x_test)

    class_order = [severity.value for severity in Severity]
    accuracy = float(accuracy_score(y_test, predictions))
    report = classification_report(
        y_test,
        predictions,
        labels=class_order,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_test, predictions, labels=class_order).tolist()
    trained_at = datetime.now(UTC).isoformat()

    bundle = {
        "model": classifier,
        "model_version": MODEL_VERSION,
        "feature_names": FEATURE_NAMES,
        "class_names": class_order,
        "trained_at_utc": trained_at,
        "training_samples": n_samples,
    }
    joblib.dump(bundle, artifact_path)

    summary = TrainingSummary(
        model_version=MODEL_VERSION,
        artifact_path=str(artifact_path),
        samples=n_samples,
        accuracy=accuracy,
        trained_at_utc=trained_at,
        classification_report=report,
        confusion_matrix=matrix,
    )
    metadata_path.write_text(
        json.dumps(summary.as_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def load_model_bundle(artifact_path: Path | None = None) -> dict[str, Any]:
    artifact_path = artifact_path or default_model_path()
    if not artifact_path.exists():
        train_model(artifact_path=artifact_path)
    bundle = joblib.load(artifact_path)
    expected = set(FEATURE_NAMES)
    actual = set(bundle.get("feature_names", []))
    if actual != expected:
        raise RuntimeError("The persisted model uses an incompatible feature schema")
    return bundle
