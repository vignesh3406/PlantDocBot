import os
import urllib.request
import json
import onnxruntime as ort

# Local path to the model files
MODEL_DIR = os.path.dirname(__file__)
LOCAL_MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.onnx")

# We will use v1.1 for the ONNX release
MODEL_URL = "https://github.com/vignesh3406/PlantDocBot/releases/download/v1.1/plant_model.onnx"

# Hardcode class mapping to avoid needing extra files
IDX_TO_CLASS = {
    0: "Pepper__bell___Bacterial_spot", 1: "Pepper__bell___healthy", 2: "Potato___Early_blight",
    3: "Potato___Late_blight", 4: "Potato___healthy", 5: "Tomato_Bacterial_spot",
    6: "Tomato_Early_blight", 7: "Tomato_Late_blight", 8: "Tomato_Leaf_Mold",
    9: "Tomato_Septoria_leaf_spot", 10: "Tomato_Spider_mites_Two_spotted_spider_mite",
    11: "Tomato__Target_Spot", 12: "Tomato__Tomato_YellowLeaf__Curl_Virus",
    13: "Tomato__Tomato_mosaic_virus", 14: "Tomato_healthy"
}

def load_model():
    """Load the ONNX model locally for plant disease classification."""
    data_url = MODEL_URL + ".data"
    data_path = LOCAL_MODEL_PATH + ".data"

    if not os.path.exists(LOCAL_MODEL_PATH) or not os.path.exists(data_path):
        print(f"[Model] Model not found locally. Downloading from {MODEL_URL} ...")
        try:
            urllib.request.urlretrieve(MODEL_URL, LOCAL_MODEL_PATH)
            urllib.request.urlretrieve(data_url, data_path)
            print("[Model] Download complete!")
        except Exception as e:
            raise FileNotFoundError(
                f"Failed to download model from {MODEL_URL}. Error: {e}\n"
                f"Please make sure BOTH 'plant_model.onnx' and 'plant_model.onnx.data' are uploaded to the v1.1 GitHub Release."
            )

    print(f"[Model] Loading local ONNX model from {LOCAL_MODEL_PATH}")
    session = ort.InferenceSession(LOCAL_MODEL_PATH)

    return session, IDX_TO_CLASS

