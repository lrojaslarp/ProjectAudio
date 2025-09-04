# Model Card (Borrador)

- **Modelo:** Clasificador logístico con estandarización
- **Tarea:** Clasificación por grupo etario aproximado a partir de rasgos acústicos
- **Datos de entrenamiento:** corpus piloto de laboratorio (describir)
- **Features:** voiced ratio, longitudes de segmentos, ZCR, centroides, MFCC; opcional SSL
- **Métricas reportadas:** Accuracy (CV=3), matriz de confusión, classification report
- **Supuestos:** calidad mínima de grabación, niños 2–6 años, tareas guiadas
- **Riesgos:** sobreajuste a ambiente; distribución no representativa
- **Limitaciones:** no clínico; requiere validación con especialistas
- **Próximos pasos:** corpus ampliado; embeddings robustos; validación externa
