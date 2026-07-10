import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.predict import router as predict_router
from routes.chat import router as chat_router

app = FastAPI(
    title="PlantDocBot API",
    description="AI-powered plant disease detection and treatment recommendation",
    version="1.0.0",
)

# Allow both local development and deployed frontend origins
allowed_origins = [
    "http://localhost:5173",        # Vite dev server
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

# Add deployed frontend URL from environment variable
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {"status": "PlantDocBot API is running 🌿"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
