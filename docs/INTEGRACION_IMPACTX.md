# Integración propuesta con ImpactX

## Ubicación del ML

El modelo debe ejecutarse inicialmente como un servicio independiente. El Galaxy Watch 8 controla
el ciclo de vida del viaje y recopila telemetría; móvil y backend transmiten o consultan eventos. El
servicio ML no inicia ni termina viajes.

## Flujo recomendado

1. El wearable detecta una señal candidata durante un viaje activo.
2. Se construye la telemetría del evento.
3. El backend o la aplicación móvil invoca `POST /api/v1/predictions/collision`.
4. El ML devuelve gravedad, confianza y acción recomendada.
5. Un motor de seguridad del backend aplica reglas finales y registra la decisión.
6. En eventos leves/moderados, el wearable muestra la cuenta regresiva.
7. En eventos graves/críticos, el backend activa inmediatamente el flujo de notificaciones.

## Contrato de ejemplo

```json
{
  "g_force_peak": 14.2,
  "heart_rate_bpm": 166,
  "impact_duration_ms": 540,
  "speed_delta_kmh": 61,
  "post_impact_inactivity_seconds": 72
}
```

La respuesta contiene `severity`, `confidence`, probabilidades por clase y `decision`.

## Producción futura

Para el prototipo local se usa Joblib. En una versión productiva se debe versionar el modelo,
registrar el esquema de características, conservar métricas por versión, validar compatibilidad y
mantener una ruta de reversión. La decisión de alerta no debe depender exclusivamente del modelo.
