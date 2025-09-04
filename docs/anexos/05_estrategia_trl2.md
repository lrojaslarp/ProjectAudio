# Estrategia para evidenciar TRL-2 (evaluación y plan)

**Objetivo:** Mostrar factibilidad técnica con resultados reproducibles y artefactos verificables.

## Evidencias clave
- Flujo reproducible de análisis → rasgos → entrenamiento (CV=3) → evaluación.
- Artefactos versionados: `model.pkl`, `feature_keys.json`, capturas y métricas.
- Documentación: README, Data Card, Model Card, CHANGELOG con línea de tiempo.

## Repositorio y accesos
- GitHub privado: main (estable), lab/piloto, exp/ssl; tags de release.
- Zenodo (opcional): DOI del *release* sin datos reales.
- Acceso a revisores mediante enlace temporal o paquete `.zip` firmado.

## Consideraciones
- No publicar audios reales; solo ejemplos sintéticos.
- Incluir en anexos capturas y `report.md` generado por `scripts/make_screenshots.py`.
- En metodología, describir la suma de *utterances* como criterio válido cuando no hay 10 s continuos.
