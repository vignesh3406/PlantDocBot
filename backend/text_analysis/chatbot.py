import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# ✅ WORKING MODEL NAME
model = genai.GenerativeModel("models/text-bison-001")


# ---------- TEXT DIAGNOSIS ----------
def text_diagnosis(user_text: str):

    prompt = f"""
    You are a plant disease expert.

    Based on this description:
    {user_text}

    Return ONLY disease name.
    """

    response = model.generate_content(prompt)

    return response.text.strip()


# ---------- AI REASONING ----------
def ai_reasoning(user_text: str):

    prompt = f"""
    Explain plant disease symptoms and treatment:

    {user_text}
    """

    response = model.generate_content(prompt)

    return response.text.strip()
