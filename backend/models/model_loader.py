import os
import torch
import urllib.request
from torchvision import models

# Local path to the model file
MODEL_DIR = os.path.dirname(__file__)
LOCAL_MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.pth")
MODEL_URL = "https://github.com/vignesh3406/PlantDocBot/releases/download/v1.0/plant_model.pth"


def load_model():
    """Load the PyTorch ResNet50 model locally for plant disease classification."""
    if not os.path.exists(LOCAL_MODEL_PATH):
        print(f"[Model] Model not found locally. Downloading from {MODEL_URL} ...")
        try:
            urllib.request.urlretrieve(MODEL_URL, LOCAL_MODEL_PATH)
            print("[Model] Download complete!")
        except Exception as e:
            raise FileNotFoundError(
                f"Failed to download model from {MODEL_URL}. Error: {e}\n"
                f"Please make sure 'plant_model.pth' is uploaded to the v1.0 GitHub Release."
            )

    print(f"[Model] Loading local model from {LOCAL_MODEL_PATH}")
    checkpoint = torch.load(LOCAL_MODEL_PATH, map_location="cpu", weights_only=False)

    state_dict = checkpoint["model_state_dict"]
    idx_to_class = checkpoint["idx_to_class"]

    num_classes = len(idx_to_class)

    model = models.resnet50(weights=None)
    model.fc = torch.nn.Linear(2048, num_classes)

    model.load_state_dict(state_dict)
    model.eval()

    return model, idx_to_class

