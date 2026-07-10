import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# A static fallback dictionary for popular plant diseases (PlantVillage dataset)
TREATMENT_MAPPING = {
    "Apple___Apple_scab": {
        "treatment": "Rake under trees and destroy infected leaves to reduce the number of fungal spores. Water in the evening or early morning (avoid overhead watering). Applications of fungicides (e.g., Captan) provide control.",
        "products": ["Captan Fungicide", "Neem Oil", "Mancozeb"]
    },
    "Apple___Black_rot": {
        "treatment": "Prune out dead or diseased branches. Remove mummified fruit. Apply a fungicide during the dormant season.",
        "products": ["Copper-based Fungicide", "Monterey Liqui-Cop"]
    },
    "Apple___healthy": {
         "treatment": "Your plant is healthy! Continue regular watering and sunlight.",
         "products": ["General Purpose Fertilizer"]
    },
    "Potato___Late_blight": {
        "treatment": "Destroy all infected plants. Apply a protectant fungicide such as chlorothalonil or copper-based sprays early in the season.",
        "products": ["Chlorothalonil Fungicide", "Copper spray"]
    },
    "Potato___healthy": {
        "treatment": "The plant appears healthy. No immediate treatment is needed.",
        "products": ["Organic Compost"]
    },
    "Tomato___Bacterial_spot": {
        "treatment": "Remove symptomatic plants from the field or greenhouse to prevent the spread. Spray with copper-based fungicides early in the infection cycle.",
        "products": ["Copper Fungicide", "Streptomycin spray"]
    },
    "Tomato___Early_blight": {
        "treatment": "Prune or stake plants to improve air circulation. Keep the soil under the plants clean. Apply appropriate fungicides.",
        "products": ["Mancozeb", "Liquid Copper Fungicide"]
    },
    "Tomato___healthy": {
        "treatment": "The tomato plant appears healthy. Ensure consistent watering.",
        "products": ["Tomato Plant Food"]
    }
}

def get_treatment(disease: str):
    """
    Returns the treatment plan and recommended products for a given disease name.
    """
    # 1. Check if we have a hardcoded treatment map for the precise class name
    if disease in TREATMENT_MAPPING:
        return TREATMENT_MAPPING[disease]
    
    # 2. Check if the disease name implies it's healthy
    if "healthy" in disease.lower() or "background" in disease.lower():
        return {
            "treatment": "The plant appears healthy. Maintain regular care.",
            "products": ["Organic Fertilizer"]
        }
        
    # 3. If an API key is present, try asking Gemini for a specific treatment
    if API_KEY:
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            prompt = f"Provide a brief treatment plan for the plant disease: '{disease}'. Also list 2-3 specific commercial products or active ingredients recommended for treatment."
            response = model.generate_content(prompt)
            return {
                "treatment": f"AI Suggestion: {response.text.strip()}",
                "products": ["See AI suggestion above"]
            }
        except Exception as e:
            pass # Fall back to default if generation fails

    # 4. Generic fallback treatment
    formatted_disease = disease.replace("_", " ").title()
    return {
        "treatment": f"The model detected '{formatted_disease}'. Prune affected leaves, avoid overhead watering, and consider applying a broad-spectrum fungicide or pesticide.",
        "products": ["Broad-spectrum Fungicide", "Neem oil", "Insecticidal soap"]
    }
