"""Safety-oriented alert policy applied after model inference."""

from __future__ import annotations

from impactx_ml.domain import AlertAction, AlertDecision, Severity, TelemetryInput


def decide_alert(
    severity: Severity,
    confidence: float,
    telemetry: TelemetryInput,
) -> AlertDecision:
    """Translate model output into an ImpactX alert action.

    Deterministic safety overrides intentionally take precedence over ML output.
    Thresholds are prototype values and require validation before real-world use.
    """
    extreme_impact = telemetry.g_force_peak >= 18 or telemetry.speed_delta_kmh >= 85
    immobility_after_strong_impact = (
        telemetry.g_force_peak >= 11 and telemetry.post_impact_inactivity_seconds >= 45
    )
    physiologic_risk = telemetry.g_force_peak >= 8 and (
        telemetry.heart_rate_bpm <= 38 or telemetry.heart_rate_bpm >= 205
    )

    if extreme_impact or immobility_after_strong_impact or physiologic_risk:
        return AlertDecision(
            action=AlertAction.IMMEDIATE,
            dispatch_alert=True,
            countdown_seconds=0,
            reason="Regla de seguridad activada por telemetría de alto riesgo.",
            safety_override=True,
        )

    if severity in {Severity.SEVERE, Severity.CRITICAL}:
        return AlertDecision(
            action=AlertAction.IMMEDIATE,
            dispatch_alert=True,
            countdown_seconds=0,
            reason="El modelo clasificó el evento como grave o crítico.",
        )

    if severity == Severity.MODERATE:
        return AlertDecision(
            action=AlertAction.COUNTDOWN_5,
            dispatch_alert=False,
            countdown_seconds=5,
            reason="Se requiere validación rápida; al vencer el tiempo se enviaría la alerta.",
        )

    if severity == Severity.MILD:
        return AlertDecision(
            action=AlertAction.COUNTDOWN_10,
            dispatch_alert=False,
            countdown_seconds=10,
            reason="Impacto leve: el wearable permitiría cancelar la alerta durante 10 segundos.",
        )

    if confidence < 0.55 and telemetry.g_force_peak >= 4:
        return AlertDecision(
            action=AlertAction.COUNTDOWN_10,
            dispatch_alert=False,
            countdown_seconds=10,
            reason="Predicción incierta con fuerza relevante; se solicita validación preventiva.",
        )

    return AlertDecision(
        action=AlertAction.NONE,
        dispatch_alert=False,
        countdown_seconds=0,
        reason="No se detectó un evento que amerite activar el protocolo de alerta.",
    )
