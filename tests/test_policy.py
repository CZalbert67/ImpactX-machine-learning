from impactx_ml.domain import AlertAction, Severity, TelemetryInput
from impactx_ml.policy import decide_alert


def test_severe_prediction_dispatches_immediate_alert():
    telemetry = TelemetryInput(g_force_peak=13, heart_rate_bpm=150)
    decision = decide_alert(Severity.SEVERE, 0.8, telemetry)
    assert decision.action == AlertAction.IMMEDIATE
    assert decision.dispatch_alert is True


def test_mild_prediction_allows_ten_second_validation():
    telemetry = TelemetryInput(g_force_peak=4.2, heart_rate_bpm=95)
    decision = decide_alert(Severity.MILD, 0.8, telemetry)
    assert decision.action == AlertAction.COUNTDOWN_10
    assert decision.countdown_seconds == 10


def test_extreme_g_force_overrides_low_severity_prediction():
    telemetry = TelemetryInput(g_force_peak=20, heart_rate_bpm=80)
    decision = decide_alert(Severity.NO_COLLISION, 0.95, telemetry)
    assert decision.action == AlertAction.IMMEDIATE
    assert decision.safety_override is True
