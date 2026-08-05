"""FastAPI adapter and local web frontend for ImpactX integrations."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from impactx_ml import __version__
from impactx_ml.domain import TelemetryInput
from impactx_ml.service import CollisionPredictionService

WEB_ROOT = Path(__file__).resolve().parent / "web"

app = FastAPI(
    title="ImpactX Collision Prediction API",
    version=__version__,
    description="API local de demostración; no validada para emergencias reales.",
)
app.mount("/static", StaticFiles(directory=WEB_ROOT), name="static")


class CollisionPredictionRequest(BaseModel):
    g_force_peak: float = Field(ge=0, le=30)
    heart_rate_bpm: int = Field(ge=25, le=240)
    impact_duration_ms: int = Field(default=100, ge=0, le=2_000)
    speed_delta_kmh: float = Field(default=0, ge=0, le=180)
    post_impact_inactivity_seconds: int = Field(default=0, ge=0, le=600)


@lru_cache(maxsize=1)
def get_service() -> CollisionPredictionService:
    return CollisionPredictionService()


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse(Path(WEB_ROOT) / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "impactx-ml", "version": __version__}


@app.post("/api/v1/predictions/collision")
def predict_collision(payload: CollisionPredictionRequest) -> dict[str, object]:
    telemetry = TelemetryInput(**payload.model_dump())
    result = get_service().predict(telemetry)
    return {
        "input": telemetry.as_dict(),
        **result.as_dict(),
        "prototype_warning": "Resultado simulado; no sustituye validación automotriz ni médica.",
    }
