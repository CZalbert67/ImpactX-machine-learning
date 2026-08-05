from impactx_ml.domain import Severity, TelemetryInput
from impactx_ml.model import train_model
from impactx_ml.service import CollisionPredictionService


def test_model_can_train_and_predict(tmp_path):
    artifact = tmp_path / "model.joblib"
    summary = train_model(
        artifact_path=artifact,
        n_samples=1_500,
        n_estimators=60,
        random_state=11,
    )
    assert artifact.exists()
    assert summary.accuracy >= 0.65

    service = CollisionPredictionService(artifact)
    result = service.predict(
        TelemetryInput(
            g_force_peak=21,
            heart_rate_bpm=205,
            impact_duration_ms=900,
            speed_delta_kmh=95,
            post_impact_inactivity_seconds=140,
        )
    )
    assert result.severity in {Severity.SEVERE, Severity.CRITICAL}
    assert result.decision.dispatch_alert is True
