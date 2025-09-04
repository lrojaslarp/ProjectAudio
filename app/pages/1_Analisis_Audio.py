import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from core.utils import load_wav, resample_if_needed
from core.vad import energy_vad, webrtc_vad_mask, mask_to_segments
from core.features import compute_spectrogram, zcr, spectral_centroid, librosa_features
from core.ssl import ssl_embedding
from core.model import load_model, dict_to_vector, load_feature_keys

st.title("Analisis de Audio y Prediccion")

uploaded = st.file_uploader("Archivo WAV", type=["wav"])
use_example = st.checkbox("Usar ejemplo (assets/sample_02.wav)", value=False)
vad_backend = st.selectbox("Metodo de VAD", ["energia (heuristico)", "webrtcvad (si disponible)"], index=0)
use_mfcc = st.checkbox("Calcular MFCC (librosa)", value=True)
use_ssl = st.checkbox("Embeddings SSL (si disponibles localmente)", value=False)
ssl_model = st.text_input("Nombre/ruta modelo SSL local", "facebook/wav2vec2-base-960h")
ssl_device = st.selectbox("Dispositivo SSL", ["cpu"], index=0)

if not uploaded and use_example:
    uploaded = open(str(Path(__file__).resolve().parent / "assets" / "sample_02.wav"), "rb")

if uploaded is not None:
    x, sr = load_wav(uploaded)
    x, sr = resample_if_needed(x, sr, 16000)

    st.subheader("1) Espectrograma")
    f, t, S = compute_spectrogram(x, sr)
    plt.figure(figsize=(8,3))
    plt.pcolormesh(t, f, 10*np.log10(S+1e-12), shading='gouraud')
    plt.ylabel('Hz'); plt.xlabel('s'); plt.title('Espectrograma (dB)')
    st.pyplot(plt.gcf()); plt.close()

    st.subheader("2) VAD y segmentos")
    if vad_backend.startswith("webrtcvad"):
        E, mask, times = webrtc_vad_mask(x, sr)
        if E is None:
            st.warning("webrtcvad no disponible; usando energia.")
            from core.vad import energy_vad
            E, mask, times = energy_vad(x, sr)
    else:
        E, mask, times = energy_vad(x, sr)

    fig, ax = plt.subplots(figsize=(8,2.2))
    ax.plot(times, E, label="Energia (dB)")
    ax.fill_between(times, -120, 40, where=mask>0, alpha=0.3, step='pre', label="Voz")
    ax.set_ylim(-90, 10); ax.set_xlabel("s"); ax.set_ylabel("dB"); ax.legend(loc="upper right")
    st.pyplot(fig); plt.close(fig)

    speech_segs = mask_to_segments(mask, times, kind=1)
    pause_segs = mask_to_segments(mask, times, kind=0)
    speech_durs = [max(0.0, b-a) for a,b in speech_segs]
    pause_durs = [max(0.0, b-a) for a,b in pause_segs]
    voiced_ratio = sum(speech_durs)/(sum(speech_durs)+sum(pause_durs)+1e-9)
    mean_speech = float(np.mean(speech_durs)) if speech_durs else 0.0
    mean_pause = float(np.mean(pause_durs)) if pause_durs else 0.0
    turns = sum(1 for _ in speech_segs)

    st.subheader("3) Rasgos")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Voiced ratio", f"{voiced_ratio:.2f}")
    with c2: st.metric("Media seg voz", f"{mean_speech:.2f} s")
    with c3: st.metric("Media pausa", f"{mean_pause:.2f} s")
    with c4: st.metric("Turnos (voz)", f"{turns}")

    z = zcr(x)
    c = spectral_centroid(x, sr)
    feat = {"voiced_ratio": voiced_ratio, "mean_speech_s": mean_speech, "mean_pause_s": mean_pause, "zcr": z, "spectral_centroid_hz": c}
    if use_mfcc:
        lib = librosa_features(x, sr)
        st.caption("MFCC disponibles" if lib is not None else "MFCC no disponibles")
        if lib is not None:
            for i, val in enumerate(lib["mfcc_mean"]):
                feat[f"mfcc{i+1}_mean"] = float(val)
            for i, val in enumerate(lib["mfcc_std"]):
                feat[f"mfcc{i+1}_std"] = float(val)
    if use_ssl:
        emb, err = ssl_embedding(x, sr, model_name_or_path=ssl_model, device=ssl_device)
        st.caption("SSL OK" if emb is not None else f"SSL no disponible: {err}")
        if emb is not None:
            # reduce dim by mean pooling over chunks of 16 values (toy)
            import numpy as np
            step = 16
            pooled = [float(np.mean(emb[i:i+step])) for i in range(0, len(emb), step)]
            for i, v in enumerate(pooled):
                feat[f"ssl_pool_{i}"] = v

    model = load_model()
    keys = load_feature_keys()
    X1 = None
    if keys is not None:
        import numpy as np
        X1 = np.array([feat.get(k, 0.0) for k in keys], dtype=float).reshape(1, -1)
    else:
        from core.model import dict_to_vector
        X1, keys_now = dict_to_vector(feat)

    st.subheader("4) Prediccion (si hay modelo)")
    if model is None:
        st.info("No hay modelo entrenado. Entrena uno en 'Entrenamiento Piloto'.")
    else:
        try:
            import numpy as np
            yhat = model.predict(X1)[0]
            proba = None
            try:
                proba = float(np.max(model.predict_proba(X1)))
            except Exception:
                pass
            st.success(f"Prediccion: {yhat} " + (f"(confianza ~{int(proba*100)}%)" if proba else ""))
        except Exception as e:
            st.error(f"No se pudo predecir con las llaves de rasgos actuales: {e}")
