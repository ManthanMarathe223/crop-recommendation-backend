from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ml_models import load_ml_models
from routers import predictions, weather, translations, reports, crops

app = FastAPI(title="Crop Recommendation API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models on startup
@app.on_event("startup")
async def startup():
    load_ml_models()

# Include routers
app.include_router(predictions.router)
app.include_router(weather.router)
app.include_router(translations.router)
app.include_router(reports.router)
app.include_router(crops.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🌾 Crop Recommendation API v2.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}