import numpy as np
from scipy.signal import spectrogram, stft

def compute_spectrogram(x, sr):
    f, t, S = spectrogram(x, fs=sr, nperseg=512, noverlap=384)
    return f, t, S

def zcr(x):
    x = np.asarray(x, dtype=float)
    return float(((x[:-1]*x[1:]) < 0).mean())

def spectral_centroid(x, sr, frame=512, hop=256):
    f, t, Z = stft(x, fs=sr, nperseg=frame, noverlap=frame-hop)
    mag = np.abs(Z)+1e-9
    centroid = np.sum(f[:,None]*mag, axis=0)/np.sum(mag, axis=0)
    return float(np.nanmean(centroid))

def librosa_features(x, sr):
    try:
        import librosa
        mfcc = librosa.feature.mfcc(y=x.astype(float), sr=sr, n_mfcc=13)
        return {"mfcc_mean": mfcc.mean(axis=1).tolist(),
                "mfcc_std": mfcc.std(axis=1).tolist()}
    except Exception:
        return None
