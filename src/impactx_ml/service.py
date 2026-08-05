"""Inference service used by the CLI, API, tests, and Streamlit UI."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from impactx_ml.domain import FEATURE_NAMES, PredictionResult, Severity, TelemetryInput
from impactx_ml.model import load_model_bundle
from impactx_ml.policy import decide_alert


class CollisionPredictionService:
    def __init__(self, artifact_path: Path | None = None) -> None:
        self._bundle = load_model_bundle(artifact_path)
        self._model = self._bundle["model"]
        self.model_version = str(self._bundle["model_version"])

    def predict(self, telemetry: TelemetryInput) -> PredictionResult:
        frame = pd.DataFrame([telemetry.as_feature_row()], columns=FEATURE_NAMES)
        predicted_label = str(self._model.predict(frame)[0])
        raw_probabilities = self._model.predict_proba(frame)[0]
        model_classes = [str(item) for item in self._model.classes_]
        probability_map = {
            label: float(probability)
            for label, probability in zip(model_classes, raw_probabilities, strict=True)
        }
        ordered_probabilities = {
            severity.value: probability_map.get(severity.value, 0.0) for severity in Severity
        }
        confidence = float(np.max(raw_probabilities))
        severity = Severity(predicted_label)
        decision = decide_alert(severity, confidence, telemetry)
        return PredictionResult(
            severity=severity,
            confidence=confidence,
            probabilities=ordered_probabilities,
            decision=decision,
            model_version=self.model_version,
        )
