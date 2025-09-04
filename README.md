
# CaLola · Laboratorio de Audio Infantil

Entorno de laboratorio para **análisis de audio**, **extracción de rasgos**, **entrenamiento piloto** y **evaluación**.
No incluye datos reales; los audios de producción deben gestionarse en almacenamiento seguro con consentimiento.

## Características
- Multipágina (Streamlit): Análisis · Entrenamiento · Evaluación · Documentos
- VAD por energía y opción **WebRTC VAD** (si está instalado `webrtcvad`)
- Rasgos: ratio de voz, segmentos/pausas, ZCR, centroide, **MFCC** (`librosa`); **embeddings SSL** opcionales
- Entrenamiento **LogisticRegression** con **CV=3** y persistencia de artefactos (`model.pkl`, `feature_keys.json`)
- Scripts de evidencia reproducible y verificación del entorno

## Requisitos
```bash
pip install -r requirements-min.txt
# Extras opcionales
pip install -r requirements-extras.txt
```

## Ejecución (local)
```bash
streamlit run app/Home.py
```

## Estructura
```
app/
  core/            # vad, features, ssl (hook), model, utils
  pages/           # 1_Analisis_Audio · 2_Entrenamiento_Piloto · 3_Evaluacion_Metricas · 4_Documentos_Laboratorio
  assets/          # audios de ejemplo (sintéticos)
  data/            # CSVs de etiquetas (ej. pilot_labels.csv)
  models/          # artefactos (model.pkl, feature_keys.json)
docs/
  anexos/          # textos listos para postulación
  TEMPLATE_*       # plantillas de Data/Model Card
scripts/
  make_screenshots.py
  verify_env.py
```

## Privacidad y uso responsable
- **No** subir audios reales al repo. `.gitignore` ya excluye `*.wav` (salvo ejemplos sintéticos).
- Mantener consentimientos y datos reales en almacenamiento seguro con control de acceso.
- Ver `docs/anexos/03_gestion_datos_etica.md` y las plantillas de Data/Model Card.

## Versionado
- Ver `CHANGELOG.md`. Hito actual: **v0.3.0-lab** (2025-09-04).

## Citar
- `CITATION.cff` incluido.
