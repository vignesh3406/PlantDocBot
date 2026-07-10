import torch
from torchvision import models

MODEL_PATH = "models/plant_model.pth"

def load_model():

    checkpoint = torch.load(MODEL_PATH, map_location="cpu")

    state_dict = checkpoint["model_state_dict"]
    idx_to_class = checkpoint["idx_to_class"]

    num_classes = len(idx_to_class)

    model = models.resnet50(weights=None)
    model.fc = torch.nn.Linear(2048, num_classes)

    model.load_state_dict(state_dict)

    model.eval()

    return model, idx_to_class
