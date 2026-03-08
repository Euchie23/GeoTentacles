# utils/model_loader.py

from pathlib import Path
import joblib

MODEL_DIR = Path("marine_toxic_tide") / "models"

def list_available_models():
    """
    Returns a dict:
    {
        pollutant: [model_names...]
    }
    """
    models = {}

    for f in MODEL_DIR.glob("*.joblib"):
        name = f.stem  # Metal_A_full_pressures
        parts = name.split("_", 2)
        if len(parts) < 3:
            print(f"⚠️ Skipping file with unexpected name: {f.name}")
            continue

        pollutant = "_".join(parts[:2])  # first two segments
        model_type = parts[2]            # rest of the name
        models.setdefault(pollutant, []).append(model_type)

    return models

@st.cache_resource
def load_model(pollutant, model_type):
    """
    Load a specific pretrained model
    """
    model_path = MODEL_DIR / f"{pollutant}_{model_type}.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    return joblib.load(model_path)
