# ImpactX Machine Learning

Primer prototipo predictivo de ImpactX para estimar la gravedad de un posible choque y decidir si
se debe omitir la alerta, solicitar validación en el wearable o activar una alerta inmediata.

> **Aviso:** esta versión se entrena con datos sintéticos. Es una demostración técnica, no un
> sistema validado para emergencias reales.

## Qué incluye

- Modelo Random Forest multiclase.
- Generador reproducible de datos sintéticos.
- Frontend local hecho con HTML, CSS y JavaScript.
- API local con FastAPI.
- Reglas de seguridad independientes del modelo.
- Entrenamiento, predicción por terminal, pruebas y CI.
- Sin Docker.

## Categorías y acciones

| Gravedad | Acción del prototipo |
|---|---|
| Sin choque | No enviar alerta |
| Leve | Permitir cancelar durante 10 segundos |
| Moderado | Validación rápida de 5 segundos |
| Grave | Alerta inmediata |
| Crítico | Alerta inmediata |

Además, una fuerza extrema, un cambio de velocidad muy alto, inmovilidad prolongada o una frecuencia
cardiaca extrema pueden activar una regla de seguridad y elevar la respuesta a alerta inmediata.

## Instalación rápida en Arch Linux

```bash
sudo pacman -S --needed git python python-pip

cd ImpactX-machine-learning
chmod +x scripts/*.sh
./scripts/bootstrap.sh
```

## Ejecutar la aplicación local

```bash
cd ImpactX-machine-learning
source .venv/bin/activate
python app.py
```

Abrir `http://127.0.0.1:8000` en el navegador. La documentación interactiva de la API está en
`http://127.0.0.1:8000/docs`.

## Ejecutar en modo de desarrollo

```bash
source .venv/bin/activate
uvicorn impactx_ml.api:app --reload
```

## Petición directa a la API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predictions/collision \
  -H 'Content-Type: application/json' \
  -d '{
    "g_force_peak": 14.0,
    "heart_rate_bpm": 170,
    "impact_duration_ms": 600,
    "speed_delta_kmh": 65,
    "post_impact_inactivity_seconds": 80
  }'
```

## Entrenar manualmente

```bash
source .venv/bin/activate
python -m impactx_ml.train --samples 15000 --trees 260
```

El modelo y sus métricas se guardan en `artifacts/`. Si el artefacto no existe, la aplicación lo
entrena automáticamente en su primer arranque.

## Predicción desde terminal

```bash
source .venv/bin/activate
impactx-predict \
  --g-force 8.2 \
  --heart-rate 132 \
  --duration-ms 280 \
  --speed-delta 32 \
  --inactivity-seconds 20
```

## Pruebas y calidad

```bash
source .venv/bin/activate
ruff check src tests app.py
ruff format --check src tests app.py
pytest --cov=impactx_ml
bandit -r src -ll -ii
pip-audit
```

## Subir cambios a GitHub

Desde una copia clonada del repositorio:

```bash
git switch -c feat/modelo-predictivo-v1
git add .
git commit -m "feat: add collision severity ML prototype"
git push -u origin feat/modelo-predictivo-v1
```

Después crea el Pull Request hacia `main` o hacia la rama definida por el equipo.

## Arquitectura

- `src/impactx_ml/dataset.py`: crea los datos sintéticos.
- `src/impactx_ml/model.py`: entrena y guarda el modelo.
- `src/impactx_ml/service.py`: ejecuta inferencias.
- `src/impactx_ml/policy.py`: decide el protocolo de alerta.
- `src/impactx_ml/api.py`: expone la API HTTP y sirve el frontend.
- `src/impactx_ml/web/`: interfaz local.
- `app.py`: arranque sencillo del servidor.
- `docs/MODEL_CARD.md`: alcance y limitaciones.
- `docs/INTEGRACION_IMPACTX.md`: integración futura.
