from fastapi.testclient import TestClient

from impactx_ml.api import app


client = TestClient(app)


def test_frontend_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "ImpactX ML" in response.text


def test_static_assets_are_served():
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "prediction-form" in response.text


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prediction_endpoint():
    response = client.post(
        "/api/v1/predictions/collision",
        json={
            "g_force_peak": 14,
            "heart_rate_bpm": 170,
            "impact_duration_ms": 600,
            "speed_delta_kmh": 65,
            "post_impact_inactivity_seconds": 80,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "severity" in body
    assert "decision" in body
