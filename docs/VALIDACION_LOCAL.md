# Validación local del prototipo

## Resultado automatizado

- Pruebas: 10 aprobadas.
- Cobertura observada: 82% del paquete `impactx_ml`.
- Muestras sintéticas de entrenamiento final: 15000.
- Exactitud sobre partición sintética de prueba: 0.9730.
- Versión del modelo: `impactx-collision-rf-v1`.

La exactitud no representa desempeño real porque entrenamiento y evaluación proceden del mismo
generador sintético. Solo confirma que la implementación aprende y reproduce el patrón simulado.

## Casos de humo

| Escenario | Resultado esperado |
|---|---|
| 1.2 G, 78 BPM | Sin choque, sin alerta |
| 4.5 G, 96 BPM | Leve, validación de 10 segundos |
| 8 G, 128 BPM | Moderado, validación de 5 segundos |
| 22 G, 210 BPM | Crítico, alerta inmediata |

También se verificaron respuestas HTTP correctas para el frontend, archivos estáticos, `/health` y
`POST /api/v1/predictions/collision`.
