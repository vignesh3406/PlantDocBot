from fastapi import APIRouter, UploadFile, File
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
import io

from models.model_loader import load_model
from treatments import get_treatment
router = APIRouter()

model, idx_to_class = load_model()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    pred_idx = torch.argmax(probs).item()

    disease = idx_to_class[pred_idx]
    confidence = float(probs[pred_idx])

    # If confidence is too low, the image is likely not a plant leaf
    if confidence < 0.40:
        return {
            "is_plant": False,
            "message": "This doesn't look like a plant leaf. Please upload a clear image of a plant leaf for accurate diagnosis."
        }

    treatment_info = get_treatment(disease)

    return {
        "is_plant": True,
        "disease": disease,
        "confidence": confidence,
        "treatment": treatment_info["treatment"],
        "products": treatment_info["products"]
    }
