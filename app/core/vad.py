import numpy as np
from scipy.signal import lfilter

def energy_vad(x, sr, frame_ms=20, hop_ms=10, thr_db=-35.0, min_speech_ms=60):
    x = np.asarray(x, dtype=float)
    if x.ndim > 1: x = x[:,0]
    x = lfilter([1, -0.97], [1], x)
    frame = int(sr * frame_ms/1000.0)
    hop = int(sr * hop_ms/1000.0)
    if frame <= 0: frame = 1
    if hop <= 0: hop = 1
    n_frames = 1 if len(x) < frame else 1 + int((len(x)-frame)//hop)
    E = []
    for i in range(n_frames):
        s = i*hop; e = s+frame
        seg = x[s:e] if e <= len(x) else x[s:]
        if seg.size == 0: E.append(-120.0); continue
        rms = np.sqrt(np.mean(seg**2) + 1e-12)
        db = 20*np.log10(rms + 1e-12)
        E.append(db)
    E = np.array(E)
    baseline = np.percentile(E, 20)
    thr = max(-90.0, baseline + thr_db)
    mask = (E > thr).astype(int)
    times = (np.arange(len(E))*hop + frame/2)/sr
    min_frames = max(1, int(min_speech_ms/hop_ms))
    i = 0
    while i < len(mask):
        if mask[i] == 1:
            j = i
            while j < len(mask) and mask[j] == 1: j += 1
            if (j - i) < min_frames: mask[i:j] = 0
            i = j
        else:
            i += 1
    return E, mask, times

def webrtc_vad_mask(x, sr, frame_ms=20, hop_ms=10, aggressiveness=2):
    try:
        import webrtcvad
        vad = webrtcvad.Vad(aggressiveness)
    except Exception:
        return None, None, None
    x = np.asarray(x, dtype=float)
    if x.ndim > 1: x = x[:,0]
    # 16-bit PCM mono required
    pcm = (np.clip(x, -1.0, 1.0)*32767).astype('<i2').tobytes()
    frame = int(sr * frame_ms/1000.0)
    hop = int(sr * hop_ms/1000.0)
    if frame % 160 != 0:
        # WebRTC VAD typical frames 10/20/30 ms at 16 kHz => 160/320/480 samples
        frame = 320; hop = 160
    n = len(x)
    idx = 0
    mask = []
    times = []
    while idx+frame <= n:
        chunk = pcm[2*idx:2*(idx+frame)]
        is_speech = 1 if vad.is_speech(chunk, sr) else 0
        mask.append(is_speech)
        times.append((idx + frame/2)/sr)
        idx += hop
    # energy per frame (rough estimate)
    E = []
    idx = 0
    while idx+frame <= n:
        seg = x[idx:idx+frame]
        rms = np.sqrt(np.mean(seg**2) + 1e-12)
        db = 20*np.log10(rms + 1e-12)
        E.append(db)
        idx += hop
    return np.array(E), np.array(mask), np.array(times)

def mask_to_segments(mask, times, kind=1):
    segs = []
    i = 0; N = len(mask)
    while i < N:
        if mask[i] == kind:
            j = i
            while j < N and mask[j] == kind: j += 1
            t0 = times[i] if i < len(times) else 0.0
            t1 = times[j-1] if j-1 < len(times) else (times[-1] if len(times)>0 else 0.0)
            segs.append((float(t0), float(t1)))
            i = j
        else:
            i += 1
    return segs
