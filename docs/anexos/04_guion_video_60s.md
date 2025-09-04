# Guion de video (60 s)

1. Pantalla Home (5 s): "Entorno de laboratorio para análisis y entrenamiento de prototipos."
2. Análisis (20 s):
   - Cargar WAV (ej. assets/sample_02.wav).
   - Mostrar espectrograma y VAD; resaltar métricas (ratio de voz, segmentos/pausas, turnos).
3. Entrenamiento (20 s):
   - Cargar CSV `app/data/pilot_labels.csv`.
   - Ejecutar extracción de rasgos y entrenamiento con CV=3; mostrar Accuracy CV.
4. Evaluación (10 s):
   - Cargar CSV de validación y mostrar matriz de confusión + resumen de métricas.
5. Cierre (5 s): "Código modular, datos seguros y documentación disponible (Data/Model Cards)."
