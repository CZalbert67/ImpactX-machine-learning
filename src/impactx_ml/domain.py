"""Domain objects shared by training, inference, API, and UI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    NO_COLLISION = "sin_choque"
    MILD = "leve"
    MODERATE = "moderado"
    SEVERE = "grave"
    CRITICAL = "critico"


class AlertAction(StrEnum):
    NONE = "sin_alerta"
    COUNTDOWN_10 = "validacion_10_segundos"
    COUNTDOWN_5 = "validacion_5_segundos"
    IMMEDIATE = "alerta_inmediata"


FEATURE_NAMES = [
    "g_force_peak",
    "heart_rate_bpm",
    "impact_duration_ms",
    "speed_delta_kmh",
    "post_impact_inactivity_seconds",
]


@dataclass(frozen=True, slots=True)
class TelemetryInput:
    g_force_peak: float
    heart_rate_bpm: int
    impact_duration_ms: int = 100
    speed_delta_kmh: float = 0.0
    post_impact_inactivity_seconds: int = 0

    def as_feature_row(self) -> list[float]:
        return [
            float(self.g_force_peak),
            float(self.heart_rate_bpm),
            float(self.impact_duration_ms),
            float(self.speed_delta_kmh),
            float(self.post_impact_inactivity_seconds),
        ]

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AlertDecision:
    action: AlertAction
    dispatch_alert: bool
    countdown_seconds: int
    reason: str
    safety_override: bool = False


@dataclass(frozen=True, slots=True)
class PredictionResult:
    severity: Severity
    confidence: float
    probabilities: dict[str, float]
    decision: AlertDecision
    model_version: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity.value,
            "confidence": self.confidence,
            "probabilities": self.probabilities,
            "decision": {
                "action": self.decision.action.value,
                "dispatch_alert": self.decision.dispatch_alert,
                "countdown_seconds": self.decision.countdown_seconds,
                "reason": self.decision.reason,
                "safety_override": self.decision.safety_override,
            },
            "model_version": self.model_version,
        }
