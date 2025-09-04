
# Model Card — Clasificador piloto (Borrador)

- **Modelo:** Pipeline `StandardScaler` + `LogisticRegression` (sklearn).
- **Tarea:** Clasificación aproximada por grupo etario (p. ej., {2_anios, 4_anios, 5_anios}) a partir de rasgos acústicos/temporales.
- **Datos:** Corpus piloto de laboratorio (ver Data Card). Audios reales almacenados fuera del repositorio, con consentimiento.
- **Conjunto de features:**
  - **Temporales:** voiced ratio, duración media de segmentos de voz, duración media de pausas, número de turnos.
  - **Espectrales:** ZCR, centroide espectral, **MFCC** (si `librosa`).
  - **Opcionales:** embeddings **SSL** (wav2vec2/HubERT) si están disponibles localmente; agregación por *mean pooling*.
- **Entrenamiento:** Validación cruzada **CV=3** (k-fold). Persistencia de `model.pkl` y `feature_keys.json`.
- **Métricas reportadas:** Accuracy CV en entrenamiento piloto; en evaluación: matriz de confusión y *classification report*.
- **Supuestos:** Español de Chile; grabaciones de ≤5 minutos por sesión; micrófono cercano; tareas breves guiadas.
- **Riesgos:** Sobreajuste a condiciones de registro; sesgos de muestreo; variación dialectal.
- **Limitaciones:** Prototipo de laboratorio; no es una herramienta diagnóstica; requiere validación con especialistas y corpus ampliado.
- **Próximos pasos:** Ampliar corpus multirregional; métricas adicionales (AUC/F1); evaluación externa; robustecer VAD (WebRTC) y features (SSL); MLOps y monitoreo de sesgos.
