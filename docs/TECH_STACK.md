# 🌿 PlantDoc AI - Technology Stack

This document outlines the complete technology stack and dependencies used to build the PlantDoc AI (Plant Bot) project. The application is a full-stack, AI-powered system that analyzes plant leaf images for diseases and provides treatment recommendations.

## Frontend (User Interface)
The frontend is designed to be lightweight, fast, and feature a minimalist, Streamlit-inspired layout.

- **Framework:** React 19
- **Build Tool:** Vite (v7)
- **Routing/State:** Native React Hooks (`useState`, `useRef`)
- **HTTP Client:** Axios (for interacting with the backend API)
- **Styling:** Vanilla CSS (Custom design system replicating Streamlit's interface)

## Backend (API Server)
The backend acts as the bridge between the user interface and the machine learning / generative models.

- **Language:** Python 3.11+
- **Framework:** FastAPI (High-performance web framework for APIs)
- **ASGI Server:** Uvicorn (For running the FastAPI application)
- **Environment Management:** `python-dotenv` (For securely loading API keys)
- **Concurrency:** Async/Await handling for fast network I/O

## Machine Learning & AI
The core intelligence of the application resides here, using a hybrid approach of a specialized vision model and a Large Language Model.

- **Deep Learning Framework:** PyTorch & TorchvisionJ
- **Vision Architecture:** ResNet50 (Fine-tuned for plant disease classification)
- **Image Processing:** Pillow (`PIL`)
- **Generative AI Integration:** Google Generative AI (`google-generativeai` package) utilizing the Gemini API for dynamic, natural-language treatment and product recommendations.

## Core Files & Structure
- `/frontend/`
  - `src/App.jsx` - Main React component handling the drag-and-drop UI and API state.
  - `src/index.css` & `src/App.css` - Custom styling tailored to specific stream-lit features.
- `/backend/`
  - `main.py` - FastAPI entry point.
  - `routes/predict.py` - Endpoint processing image uploads through PyTorch.
  - `treatments.py` - Fallback logic and Gemini integration.
  - `models/model_loader.py` - Handles dynamic loading of `plant_model.pth`.
