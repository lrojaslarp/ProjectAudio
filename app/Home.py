import streamlit as st

st.set_page_config(page_title="CaLola · Laboratorio", page_icon="🧪", layout="wide")
st.title("CaLola · Laboratorio de Audio Infantil")

st.write("""
Entorno multipagina para trabajo de laboratorio: analisis de audio, preprocesamiento, extraccion de rasgos,
entrenamiento piloto y evaluacion con metricas estandar.
""")

st.info("Sugerencia: agrega audios reales (con consentimiento) y etiquetas para entrenar un modelo piloto.")
