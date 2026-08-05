#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m impactx_ml.train

echo
echo "Instalación terminada."
echo "Aplicación: source .venv/bin/activate && python app.py"
echo "API:      source .venv/bin/activate && uvicorn impactx_ml.api:app --reload"
