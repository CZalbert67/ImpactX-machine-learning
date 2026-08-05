"""CLI for local, scriptable predictions."""

from __future__ import annotations

import argparse
import json

from impactx_ml.domain import TelemetryInput
from impactx_ml.service import CollisionPredictionService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Predice la gravedad de un posible choque")
    parser.add_argument("--g-force", type=float, required=True)
    parser.add_argument("--heart-rate", type=int, required=True)
    parser.add_argument("--duration-ms", type=int, default=100)
    parser.add_argument("--speed-delta", type=float, default=0)
    parser.add_argument("--inactivity-seconds", type=int, default=0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    telemetry = TelemetryInput(
        g_force_peak=args.g_force,
        heart_rate_bpm=args.heart_rate,
        impact_duration_ms=args.duration_ms,
        speed_delta_kmh=args.speed_delta,
        post_impact_inactivity_seconds=args.inactivity_seconds,
    )
    result = CollisionPredictionService().predict(telemetry)
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
