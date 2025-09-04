import numpy as np
import soundfile as sf

def load_wav(fileobj_or_path):
    x, sr = sf.read(fileobj_or_path, dtype="float32", always_2d=False)
    if hasattr(x, 'ndim') and x.ndim > 1:
        x = x[:,0]
    return x, int(sr)

def resample_if_needed(x, sr, target_sr=16000):
    if sr == target_sr:
        return x, sr
    try:
        import librosa
        xr = librosa.resample(x, orig_sr=sr, target_sr=target_sr)
        return xr.astype("float32"), target_sr
    except Exception:
        return x.astype("float32"), sr
