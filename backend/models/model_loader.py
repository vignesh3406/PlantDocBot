import os
import torch
from torchvision import models

# Local path to the model file
MODEL_DIR = os.path.dirname(__file__)
LOCAL_MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.pth")


def load_model():
    """Load the PyTorch ResNet50 model locally for plant disease classification."""
    if not os.path.exists(LOCAL_MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at local path: '{LOCAL_MODEL_PATH}'. "
            f"Please make sure 'plant_model.pth' is inside the 'backend/models/' folder."
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

