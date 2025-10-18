from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import numpy as np

app = FastAPI(title="Crop Recommendation API")

# Enable CORS (allows frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will restrict this to Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
crop_model = None
yield_model = None
price_model = None
scaler = None
label_encoder = None
crop_data = None

# Load and train models when server starts
@app.on_event("startup")
async def load_models():
    global crop_model, yield_model, price_model, scaler, label_encoder, crop_data
    
    try:
        # Load Excel data
        crop_data = pd.read_excel("Updated_Crop_Yield_Prediction.xlsx")
        print(f"✅ Loaded {len(crop_data)} rows of crop data")
        
        # Prepare features and targets
        X = crop_data[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 
                        'Humidity', 'pH_Value', 'Rainfall']]
        y_crop = crop_data['Crop']
        y_yield = crop_data['Yield']
        y_price = crop_data['Price']
        
        # Encode crop names
        label_encoder = LabelEncoder()
        y_crop_encoded = label_encoder.fit_transform(y_crop)
        
        # Scale features for crop prediction
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train Crop Prediction Model
        crop_model = RandomForestClassifier(n_estimators=100, random_state=42)
        crop_model.fit(X_scaled, y_crop_encoded)
        print("✅ Crop prediction model trained")
        
        # Train Yield Prediction Model
        yield_model = RandomForestRegressor(n_estimators=100, random_state=42)
        yield_model.fit(X, y_yield)
        print("✅ Yield prediction model trained")
        
        # Train Price Prediction Model
        price_model = RandomForestRegressor(n_estimators=100, random_state=42)
        price_model.fit(X, y_price)
        print("✅ Price prediction model trained")
        
        print("🚀 All models loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        raise e

# Input data structure
class CropInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph_value: float
    rainfall: float

# Response structure
class CropPrediction(BaseModel):
    crop: str
    confidence: float
    yield_kg_per_hectare: float
    price_per_quintal: float
    estimated_revenue: float

# Root endpoint (health check)
@app.get("/")
async def root():
    return {
        "message": "🌾 Crop Recommendation API is running!",
        "version": "1.0",
        "endpoints": ["/predict", "/predict-top-3", "/crops"]
    }

# Single crop prediction
@app.post("/predict", response_model=dict)
async def predict_crop(data: CropInput):
    try:
        # Prepare input
        input_data = [[
            data.nitrogen, data.phosphorus, data.potassium,
            data.temperature, data.humidity, data.ph_value, data.rainfall
        ]]
        
        # Scale input for crop prediction
        input_scaled = scaler.transform(input_data)
        
        # Predict crop
        crop_encoded = crop_model.predict(input_scaled)[0]
        crop_name = label_encoder.inverse_transform([crop_encoded])[0]
        
        # Get prediction confidence
        crop_proba = crop_model.predict_proba(input_scaled)[0]
        confidence = float(np.max(crop_proba) * 100)
        
        # Predict yield and price
        predicted_yield = float(yield_model.predict(input_data)[0])
        predicted_price = float(price_model.predict(input_data)[0])
        
        # Calculate revenue (formula from original code)
        revenue = 0.01 * predicted_yield * predicted_price
        
        return {
            "success": True,
            "crop": crop_name,
            "confidence": round(confidence, 2),
            "yield_kg_per_hectare": round(predicted_yield, 2),
            "price_per_quintal": round(predicted_price, 2),
            "estimated_revenue": round(revenue, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-top-3")
async def predict_top_crops(data: CropInput):
    try:
        input_data = [[
            data.nitrogen, data.phosphorus, data.potassium,
            data.temperature, data.humidity, data.ph_value, data.rainfall
        ]]
        
        input_scaled = scaler.transform(input_data)
        probabilities = crop_model.predict_proba(input_scaled)[0]
        
        # Get ALL crops sorted by probability
        all_indices = probabilities.argsort()[::-1]
        
        results = []
        seen_crops = set()  # Track unique crops
        
        # Keep adding until we have 3 DIFFERENT crops
        for idx in all_indices:
            crop_name = label_encoder.inverse_transform([idx])[0]
            
            # Skip if we already added this crop
            if crop_name in seen_crops:
                continue
                
            seen_crops.add(crop_name)
            confidence = float(probabilities[idx] * 100)
            
            # Get crop-specific data
            crop_specific_data = crop_data[crop_data['Crop'] == crop_name]
            
            if not crop_specific_data.empty:
                predicted_yield = float(crop_specific_data['Yield'].mean())
                predicted_price = float(crop_specific_data['Price'].mean())
            else:
                predicted_yield = float(yield_model.predict(input_data)[0])
                predicted_price = float(price_model.predict(input_data)[0])
            
            revenue = 0.01 * predicted_yield * predicted_price
            
            results.append({
                "crop": crop_name,
                "confidence": round(confidence, 2),
                "yield_kg_per_hectare": round(predicted_yield, 2),
                "price_per_quintal": round(predicted_price, 2),
                "estimated_revenue": round(revenue, 2)
            })
            
            # Stop after 3 unique crops
            if len(results) == 3:
                break
        
        return {
            "success": True,
            "top_crops": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# Get list of all available crops
@app.get("/crops")
async def get_crops():
    try:
        crops = sorted(crop_data['Crop'].unique().tolist())
        return {
            "success": True,
            "total_crops": len(crops),
            "crops": crops
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": all([
            crop_model is not None,
            yield_model is not None,
            price_model is not None
        ])
    }