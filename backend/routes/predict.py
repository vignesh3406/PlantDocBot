from fastapi import APIRouter, UploadFile, File
from PIL import Image
import numpy as np
import io
import math

from models.model_loader import load_model
from treatments import get_treatment

router = APIRouter()

# Load the ONNX session
session, idx_to_class = load_model()

def preprocess_image(image: Image.Image) -> np.ndarray:
    # Resize to 224x224
    image = image.resize((224, 224), Image.Resampling.BILINEAR)
    
    # Convert to numpy array and scale to [0, 1]
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Transpose to Channel, Height, Width (C, H, W)
    img_array = np.transpose(img_array, (2, 0, 1))
    
    # Normalize with ImageNet stats
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3, 1, 1)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3, 1, 1)
    img_array = (img_array - mean) / std
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=1, keepdims=True)

@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Preprocess image
    img_tensor = preprocess_image(image)

    # Run ONNX inference
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img_tensor})
    
    # Apply softmax to get probabilities
    probs = softmax(outputs[0])[0]

    pred_idx = int(np.argmax(probs))

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
