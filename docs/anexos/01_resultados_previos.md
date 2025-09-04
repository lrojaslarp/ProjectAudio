# Resultados de laboratorio (previos)

- Se implementó un entorno multipágina para análisis de audio infantil, con:
  - Espectrograma, VAD (energía / WebRTC), métricas de turn-taking (ratio de voz, duración de segmentos/pausas, turnos).
  - Extracción de rasgos (ZCR, centroide espectral, MFCC) y compatibilidad con embeddings SSL locales.
  - Entrenamiento piloto con validación cruzada (CV=3) y persistencia de artefactos (`model.pkl`, `feature_keys.json`).
  - Evaluación con matriz de confusión y *classification report*.

- Se generaron evidencias reproducibles (ver `scripts/make_screenshots.py`):
  - `espectrograma.png`, `vad.png`, `metrics.json`, `report.md`.

- Los audios reales se mantienen en almacenamiento seguro, con consentimientos y sin subirse al repositorio.
