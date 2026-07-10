# 🌿 PlantDocBot — AI Plant Disease Diagnosis

An AI-powered full-stack application that analyzes plant leaf images and text descriptions to diagnose diseases and recommend treatments.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi)
![PyTorch](https://img.shields.io/badge/PyTorch-ResNet50-EE4C2C?logo=pytorch)

## Features

- **📷 Image Diagnosis** — Upload a plant leaf photo and get instant disease detection using a fine-tuned ResNet50 model
- **💬 Text Diagnosis** — Describe plant symptoms in natural language and get AI-powered diagnosis via Gemini
- **💊 Treatment Recommendations** — Get specific treatment plans and product suggestions for detected diseases
- **⚡ Fast & Modern** — React 19 frontend with Vite, FastAPI backend with async support

## Project Structure

```
PlantDocBot/
├── README.md               # This file
├── render.yaml             # Render deployment blueprint
├── .gitignore
│
├── backend/                # FastAPI backend
│   ├── main.py             # App entry point
│   ├── treatments.py       # Disease → treatment mapping + Gemini AI fallback
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Container config for deployment
│   ├── models/
│   │   └── model_loader.py # PyTorch model loading + HuggingFace download
│   └── routes/
│       ├── predict.py      # POST /predict — image-based diagnosis
│       └── chat.py         # POST /chat — text-based diagnosis
│
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx         # Main UI component
│   │   ├── App.css         # Styling
│   │   └── main.jsx        # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── docs/
    └── TECH_STACK.md       # Detailed technology documentation
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Create .env file with your API key
echo GEMINI_API_KEY=your_key_here > .env

# Run the API server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status check |
| `GET` | `/health` | Health check for deployment |
| `POST` | `/predict` | Upload a leaf image for disease detection |
| `POST` | `/chat` | Send text symptoms for AI diagnosis |

## Deployment

This project is configured for **Render** with a one-click Blueprint (`render.yaml`).

The ML model (~90MB) is hosted on **HuggingFace Hub** and auto-downloaded at startup.

See [TECH_STACK.md](docs/TECH_STACK.md) for full technology details.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite 7, Axios |
| Backend | FastAPI, Uvicorn, Python 3.11+ |
| ML Model | PyTorch, ResNet50 (fine-tuned on PlantVillage) |
| AI Chat | Google Gemini API |
| Deployment | Render, Docker, HuggingFace Hub |

## License

This project is for educational purposes.
