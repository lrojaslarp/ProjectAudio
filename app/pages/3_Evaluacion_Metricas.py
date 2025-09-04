import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from core.model import load_model, load_feature_keys
from core.utils import load_wav, resample_if_needed
from core.vad import energy_vad, mask_to_segments
from core.features import zcr, spectral_centroid, librosa_features

st.title("Evaluacion y metricas")

uploaded = st.file_uploader("CSV de evaluacion (filepath,label)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    model = load_model()
    keys = load_feature_keys()
    if model is None or keys is None:
        st.error("Falta modelo o llaves de rasgos. Entrena en la seccion anterior.")
    else:
        y_true = []
        y_pred = []
        for _, row in df.iterrows():
            from pathlib import Path
            p = Path(row["filepath"])
            try:
                x, sr = load_wav(str(p))
                x, sr = resample_if_needed(x, sr, 16000)
            except Exception as e:
                st.warning(f"No se pudo leer {p}: {e}")
                continue
            E, mask, times = energy_vad(x, sr)
            speech_segs = mask_to_segments(mask, times, kind=1)
            pause_segs = mask_to_segments(mask, times, kind=0)
            speech_durs = [max(0.0, b-a) for a,b in speech_segs]
            pause_durs = [max(0.0, b-a) for a,b in pause_segs]
            voiced_ratio = sum(speech_durs)/(sum(speech_durs)+sum(pause_durs)+1e-9)
            mean_speech = float(np.mean(speech_durs)) if speech_durs else 0.0
            mean_pause = float(np.mean(pause_durs)) if pause_durs else 0.0
            z = zcr(x); c = spectral_centroid(x, sr)
            feat = {"voiced_ratio": voiced_ratio, "mean_speech_s": mean_speech, "mean_pause_s": mean_pause, "zcr": z, "spectral_centroid_hz": c}
            lib = librosa_features(x, sr)
            if lib is not None:
                for i, val in enumerate(lib["mfcc_mean"]):
                    feat[f"mfcc{i+1}_mean"] = float(val)
                for i, val in enumerate(lib["mfcc_std"]):
                    feat[f"mfcc{i+1}_std"] = float(val)
            import numpy as np
            X1 = np.array([feat.get(k, 0.0) for k in keys], dtype=float).reshape(1,-1)
            yhat = model.predict(X1)[0]
            y_true.append(row["label"]); y_pred.append(yhat)
        if y_true:
            labels = sorted(list(set(y_true + y_pred)))
            cm = confusion_matrix(y_true, y_pred, labels=labels)
            fig, ax = plt.subplots(figsize=(4,4))
            disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
            disp.plot(ax=ax, colorbar=False)
            st.pyplot(fig); plt.close(fig)
            st.subheader("Reporte")
            st.text(classification_report(y_true, y_pred, labels=labels))
        else:
            st.warning("No se generaron predicciones.")
