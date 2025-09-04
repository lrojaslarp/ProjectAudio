## Metodología de laboratorio

1. **Adquisición y preprocesamiento**
   - Ingesta de WAV mono 16 kHz; resampleo en caso necesario.
   - Detección de actividad de voz mediante umbral de energía; alternativa WebRTC VAD.
   - Segmentación en habla/pausa y cálculo de métricas de turn-taking.

2. **Extracción de rasgos**
   - Rasgos temporales: ratio de voz, duración media de segmentos/pausas, número de turnos.
   - Rasgos espectrales: ZCR, centroide; MFCC (si `librosa`).
   - Embeddings SSL locales opcionales (wav2vec2/HubERT) con reducción por *mean pooling*.

3. **Entrenamiento piloto y evaluación**
   - Vectorización consistente de rasgos y entrenamiento con validación cruzada (CV=3).
   - Persistencia de artefactos y llaves de features para predicción coherente.
   - Evaluación con matriz de confusión y *classification report* sobre conjunto de validación.

4. **Buenas prácticas**
   - Separación de dependencias mínimas y extras.
   - Exclusión de datos reales del control de versiones (.gitignore).
   - Plantillas de *Data/Model Card* y guías de privacidad y ética.
