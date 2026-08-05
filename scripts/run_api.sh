#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
uvicorn impactx_ml.api:app --reload --host 127.0.0.1 --port 8000
