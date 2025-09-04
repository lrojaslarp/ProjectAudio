import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
from core.utils import load_wav, resample_if_needed
from core.vad import energy_vad, mask_to_segments
from core.features import zcr, spectral_centroid, librosa_features
from core.ssl import ssl_embedding
from core.model import train_model, save_model

st.title("Entrenamiento Piloto")

st.write("Usa un CSV con columnas 'filepath,label'. Ejemplo: 'app/data/pilot_labels.csv'.")

root_dir = st.text_input("Carpeta raiz", "app")
csv_file = st.text_input("CSV etiquetas", "app/data/pilot_labels.csv")
use_mfcc = st.checkbox("Incluir MFCC", value=True)
use_ssl = st.checkbox("Incluir SSL (si disponibles)", value=False)
ssl_model = st.text_input("Modelo SSL local", "facebook/wav2vec2-base-960h")
ssl_device = st.selectbox("Dispositivo SSL", ["cpu"], index=0)

if st.button("Cargar y extraer rasgos"):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        st.error(f"No se pudo leer el CSV: {e}")
        st.stop()
    feats = []
    labels = []
    for _, row in df.iterrows():
        p = Path(root_dir) / row["filepath"]
        try:
            x, sr = load_wav(str(p))
            x, sr = resample_if_needed(x, sr, 16000)
        except Exception as e:
            st.warning(f"No se pudo leer {p}: {e}")
            continue
        # Simple VAD para rasgos temporales
        E, mask, times = energy_vad(x, sr)
        from core.vad import mask_to_segments
        speech_segs = mask_to_segments(mask, times, kind=1)
        pause_segs = mask_to_segments(mask, times, kind=0)
        speech_durs = [max(0.0, b-a) for a,b in speech_segs]
        pause_durs = [max(0.0, b-a) for a,b in pause_segs]
        voiced_ratio = sum(speech_durs)/(sum(speech_durs)+sum(pause_durs)+1e-9)
        mean_speech = float(np.mean(speech_durs)) if speech_durs else 0.0
        mean_pause = float(np.mean(pause_durs)) if pause_durs else 0.0
        z = zcr(x); c = spectral_centroid(x, sr)
        feat = {"voiced_ratio": voiced_ratio, "mean_speech_s": mean_speech, "mean_pause_s": mean_pause, "zcr": z, "spectral_centroid_hz": c}
        if use_mfcc:
            lib = librosa_features(x, sr)
            if lib is not None:
                for i, val in enumerate(lib["mfcc_mean"]):
                    feat[f"mfcc{i+1}_mean"] = float(val)
                for i, val in enumerate(lib["mfcc_std"]):
                    feat[f"mfcc{i+1}_std"] = float(val)
        if use_ssl:
            emb, err = ssl_embedding(x, sr, model_name_or_path=ssl_model, device=ssl_device)
            if emb is not None:
                import numpy as np
                step = 16
                pooled = [float(np.mean(emb[i:i+step])) for i in range(0, len(emb), step)]
                for i, v in enumerate(pooled):
                    feat[f"ssl_pool_{i}"] = v
            else:
                st.caption(f"SSL no disponible para {p}: {err}")
        feats.append(feat); labels.append(row["label"])
    if not feats:
        st.error("No se extrajeron rasgos.")
        st.stop()
    keys = sorted(set().union(*[set(f.keys()) for f in feats]))
    import numpy as np
    X = np.array([[f.get(k, 0.0) for k in keys] for f in feats], dtype=float)
    y = np.array(labels)
    st.success(f"Rasgos extraidos: X={X.shape}, y={y.shape}")
    st.session_state["X"] = X; st.session_state["y"] = y; st.session_state["keys"] = keys

if "X" in st.session_state and st.button("Entrenar (CV=3)"):
    model, scores = train_model(st.session_state["X"], st.session_state["y"], cv=3)
    save_model(model, st.session_state.get("keys", []))
    import numpy as np
    st.success(f"Modelo guardado. Accuracy CV: {np.mean(scores):.3f} +/- {np.std(scores):.3f}")
