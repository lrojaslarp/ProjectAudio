
"""
Script de verificación de entorno.
Genera `reports/env_report.json` y `reports/env_report.md`.
Uso:
  python scripts/verify_env.py
"""
import json, sys, platform
from pathlib import Path

packages = [
    "numpy","scipy","matplotlib","soundfile","librosa","scikit_learn",
    "webrtcvad","torch","torchaudio","transformers","joblib","pydub","streamlit"
]

def check(pkg):
    try:
        if pkg == "scikit_learn":
            import sklearn as m
        else:
            m = __import__(pkg)
        return {"ok": True, "version": getattr(m, "__version__", "n/a")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def main():
    info = {
        "python": sys.version.replace("\n"," "),
        "platform": platform.platform(),
        "packages": {p: check(p) for p in packages}
    }
    out_dir = Path("reports"); out_dir.mkdir(exist_ok=True, parents=True)
    (out_dir / "env_report.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    # MD
    lines = ["# Environment Report", "", f"- Python: {info['python']}", f"- Platform: {info['platform']}", "", "## Packages"]
    for p, st in info["packages"].items():
        if st.get("ok"):
            lines.append(f"- {p}: OK (v{st.get('version')})")
        else:
            lines.append(f"- {p}: MISSING/ERR — {st.get('error')}")
    (out_dir / "env_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Environment report written to reports/env_report.json and reports/env_report.md")

if __name__ == "__main__":
    main()
