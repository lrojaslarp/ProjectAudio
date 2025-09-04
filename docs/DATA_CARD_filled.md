
# Data Card — Corpus piloto de laboratorio CaLola (Borrador)

- **Nombre del dataset:** Corpus piloto de laboratorio CaLola
- **Propósito:** Experimentación en laboratorio para analizar patrones temporales y rasgos acústicos del habla infantil (2–6 años) y su interacción con adultos (turn-taking), como insumo para prototipos de apoyo a pesquisa/seguimiento del desarrollo del lenguaje.
- **Origen y consentimiento:** 
  - *Ejemplos sintéticos* incluidos en `app/assets/`.
  - *Audios reales (por incorporar)*: capturados en establecimientos educacionales (sala cuna, jardín, preescolar) y/o APS (CESFAM) con **consentimiento informado** de cuidadores, protocolo de anonimización y resguardo de datos.
- **Rango etario:** 2–6 años (segmentación por grupos: 2, 3, 4, 5–6).
- **Contextos:** Aula (juego guiado, lectura compartida), hogar (interacciones cotidianas), CESFAM/APS (sesiones breves).
- **Calidad acústica esperada:** Nivel de ruido bajo–medio; registro cercano a micrófono (smartphone/tablet); formato WAV 16 kHz mono.
- **Estructura de los datos:** Clips WAV + metadatos mínimos (edad/año cumplido, contexto, tarea, comuna/establecimiento anon.), timestamp y hash de consentimiento.
- **Procesamiento inicial:** 
  - Resampleo a 16 kHz; normalización [-1, 1].
  - VAD por **energía** (umbral adaptativo) u **opcional WebRTC VAD**.
  - Segmentación en habla/pausa; **criterio de validez** por *suma de utterances* (p. ej., ≥10–12 s totales aun sin tramo continuo ≥10 s).
- **Riesgos / sesgos:** Sobre/infra-representación territorial o sociocultural; variabilidad de ruido; dialectos y ritmos de interacción; sesgo de tarea.
- **Limitaciones:** Conjunto pequeño y no clínico; no generaliza sin validación formal; no diagnóstico.
- **Custodia y accesos:** Almacenamiento seguro (Drive/S3 privado con control de acceso). Acceso sólo a equipo autorizado. No se versionan audios reales en Git. Retención condicionada al consentimiento y normativa local.
