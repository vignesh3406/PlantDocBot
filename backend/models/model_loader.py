import os
import torch
from torchvision import models
from huggingface_hub import hf_hub_download

# --- Configuration ---
# IMPORTANT: Replace this with your actual HuggingFace repo ID
# after uploading the model (e.g., "vignesh3406/plantdocbot-model")
HF_REPO_ID = os.getenv("HF_MODEL_REPO", "vignesh3406/plantdocbot-model")
HF_FILENAME = "plant_model.pth"

# Local path to cache the downloaded model
MODEL_DIR = os.path.join(os.path.dirname(__file__))
LOCAL_MODEL_PATH = os.path.join(MODEL_DIR, HF_FILENAME)


def _download_model():
    """Download model from HuggingFace Hub if not cached locally."""
    if os.path.exists(LOCAL_MODEL_PATH):
        print(f"[Model] Found local model at {LOCAL_MODEL_PATH}")
        return LOCAL_MODEL_PATH

    print(f"[Model] Downloading model from HuggingFace: {HF_REPO_ID}/{HF_FILENAME}")
    try:
        downloaded_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_FILENAME,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
        )
        print(f"[Model] Downloaded successfully to {downloaded_path}")
        return downloaded_path
    except Exception as e:
        print(f"[Model] ERROR downloading model: {e}")
        # Fall back to local path in case it exists in a different location
        fallback = os.path.join(MODEL_DIR, HF_FILENAME)
        if os.path.exists(fallback):
            return fallback
        raise FileNotFoundError(
            f"Model file not found locally and could not download from "
            f"HuggingFace repo '{HF_REPO_ID}'. Please ensure the repo exists "
            f"and the model file '{HF_FILENAME}' is uploaded."
        )


def load_model():
    """Load the PyTorch ResNet50 model for plant disease classification."""
    model_path = _download_model()

    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)

    state_dict = checkpoint["model_state_dict"]
    idx_to_class = checkpoint["idx_to_class"]

    num_classes = len(idx_to_class)

    model = models.resnet50(weights=None)
    model.fc = torch.nn.Linear(2048, num_classes)

    model.load_state_dict(state_dict)
    model.eval()

    return model, idx_to_class
