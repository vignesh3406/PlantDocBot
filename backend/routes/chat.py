import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# --- Optional: Gemini AI for smarter diagnosis ---
_gemini_model = None
try:
    import google.generativeai as genai
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        _gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")
except ImportError:
    pass


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    disease: str
    source: str  # "ai" or "keyword"


# --- Keyword-based fallback ---
def _keyword_diagnosis(symptoms: str) -> str:
    """Simple keyword matching for offline/fallback diagnosis."""
    text = symptoms.lower()

    if "yellow" in text and "spots" in text:
        return "Leaf Spot Disease"
    elif "brown" in text and ("circle" in text or "spot" in text):
        return "Early Blight"
    elif "wilting" in text or "wilt" in text:
        return "Wilt Disease"
    elif "rotten" in text or "water stress" in text:
        return "Possible Root or Water Stress"
    elif "holes" in text:
        return "Pest Attack"
    elif "white" in text and "powder" in text:
        return "Powdery Mildew"
    elif "black" in text and "spot" in text:
        return "Black Spot Disease"
    elif "curl" in text and "leaf" in text:
        return "Leaf Curl Virus"
    else:
        return "Unknown Disease"


# --- AI-powered diagnosis ---
async def _ai_diagnosis(user_text: str) -> str | None:
    """Use Gemini AI for smarter text-based diagnosis."""
    if not _gemini_model:
        return None

    try:
        prompt = f"""You are a plant disease expert.

Based on this description of plant symptoms:
{user_text}

Return ONLY the disease name. No explanation."""

        response = _gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None


@router.post("/chat", response_model=ChatResponse)
async def chat_diagnosis(req: ChatRequest):
    """
    Text-based plant disease diagnosis.
    Uses Gemini AI if available, falls back to keyword matching.
    """
    # Try AI diagnosis first
    ai_result = await _ai_diagnosis(req.message)
    if ai_result:
        return ChatResponse(disease=ai_result, source="ai")

    # Fall back to keyword matching
    keyword_result = _keyword_diagnosis(req.message)
    return ChatResponse(disease=keyword_result, source="keyword")
