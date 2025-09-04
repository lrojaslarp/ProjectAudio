# CLI para generar imagenes base (espectrograma, VAD) y un reporte .md
import argparse, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from app.core.utils import load_wav, resample_if_needed
from app.core.vad import energy_vad, mask_to_segments
from app.core.features import compute_spectrogram, zcr, spectral_centroid, librosa_features

def main(audio_path, out_dir):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    x, sr = load_wav(audio_path); x, sr = resample_if_needed(x, sr, 16000)
    # Spectrogram
    f, t, S = compute_spectrogram(x, sr)
    plt.figure(figsize=(8,3))
    plt.pcolormesh(t, f, 10*np.log10(S+1e-12), shading='gouraud')
    plt.ylabel('Hz'); plt.xlabel('s'); plt.title('Espectrograma (dB)')
    plt.tight_layout(); plt.savefig(out / 'spectrogram.png', dpi=160); plt.close()
    # VAD
    E, mask, times = energy_vad(x, sr)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8,2.2))
    ax.plot(times, E, label='Energia (dB)')
    ax.fill_between(times, -120, 40, where=mask>0, alpha=0.3, step='pre', label='Voz')
    ax.set_ylim(-90, 10); ax.set_xlabel('s'); ax.set_ylabel('dB'); ax.legend(loc='upper right')
    plt.tight_layout(); plt.savefig(out / 'vad.png', dpi=160); plt.close(fig)
    # Metrics
    speech_segs = mask_to_segments(mask, times, kind=1)
    pause_segs = mask_to_segments(mask, times, kind=0)
    speech_durs = [max(0.0, b-a) for a,b in speech_segs]
    pause_durs = [max(0.0, b-a) for a,b in pause_segs]
    metrics = {
        "voiced_ratio": float(sum(speech_durs)/(sum(speech_durs)+sum(pause_durs)+1e-9)),
        "mean_speech_s": float(np.mean(speech_durs) if speech_durs else 0.0),
        "mean_pause_s": float(np.mean(pause_durs) if pause_durs else 0.0),
        "zcr": float(zcr(x)),
        "spectral_centroid_hz": float(spectral_centroid(x, sr))
    }
    (out / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    # Report
    (out / 'report.md').write_text(
        f"""# Reporte de laboratorio\n\n![Espectrograma](spectrogram.png)\n\n![VAD](vad.png)\n\n## Metricas\n```json\n{json.dumps(metrics, indent=2)}\n```\n""",
        encoding='utf-8'
    )

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--audio', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    main(args.audio, args.out)
