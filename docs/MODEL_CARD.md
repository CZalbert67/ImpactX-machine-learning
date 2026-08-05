# Model Card — ImpactX Collision RF v1

## Objetivo

Demostrar un flujo completo para clasificar un evento vehicular en cinco categorías:
`sin_choque`, `leve`, `moderado`, `grave` y `critico`.

## Entradas

1. Fuerza máxima del impacto en G.
2. Frecuencia cardiaca en BPM.
3. Duración estimada del impacto en milisegundos.
4. Cambio de velocidad en km/h.
5. Inactividad posterior al impacto en segundos.

## Modelo

Random Forest multiclase. El artefacto se crea localmente en `artifacts/` y no se versiona.

## Datos

La versión v1 se entrena únicamente con datos sintéticos generados por distribuciones con
solapamiento. Esto permite probar código, endpoints y experiencia de usuario, pero no medir el
rendimiento real del detector.

## Política de alertas

- Sin choque: no enviar alerta.
- Leve: validación de 10 segundos.
- Moderado: validación de 5 segundos.
- Grave o crítico: alerta inmediata.
- Reglas determinísticas pueden elevar cualquier predicción a alerta inmediata.

## Limitaciones críticas

- Los umbrales no han sido validados con pruebas de choque, datos de vehículos ni estudios médicos.
- El BPM aislado no demuestra lesión ni gravedad.
- El modelo no debe desplegarse como único mecanismo de seguridad.
- Antes de producción se requieren datos reales anonimizados, revisión ética/legal, calibración por
  dispositivo, análisis de falsos negativos y pruebas de campo controladas.
