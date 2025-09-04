import json, numpy as np
from pathlib import Path
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"
FEATURES_JSON = MODEL_DIR / "feature_keys.json"

def dict_to_vector(d):
    keys = sorted(d.keys())
    x = np.array([d[k] for k in keys], dtype=float)
    return x, keys

def train_model(X, y, cv=3):
    clf = Pipeline([("scaler", StandardScaler()), ("logreg", LogisticRegression(max_iter=200))])
    scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
    clf.fit(X, y)
    return clf, scores.tolist()

def save_model(model, feature_keys):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    dump(model, MODEL_PATH)
    FEATURES_JSON.write_text(json.dumps(feature_keys, indent=2), encoding="utf-8")

def load_model():
    if MODEL_PATH.exists():
        return load(MODEL_PATH)
    return None

def load_feature_keys():
    if FEATURES_JSON.exists():
        import json
        return json.loads(FEATURES_JSON.read_text(encoding="utf-8"))
    return None
