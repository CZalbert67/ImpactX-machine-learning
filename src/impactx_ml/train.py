"""Command-line model training entry point."""

from __future__ import annotations

import argparse
import json

from impactx_ml.model import train_model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Entrena el primer modelo de ImpactX")
    parser.add_argument("--samples", type=int, default=15_000)
    parser.add_argument("--trees", type=int, default=260)
    parser.add_argument("--seed", type=int, default=42)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = train_model(
        n_samples=args.samples,
        n_estimators=args.trees,
        random_state=args.seed,
    )
    print(json.dumps(summary.as_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
