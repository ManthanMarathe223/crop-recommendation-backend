from fastapi import APIRouter, HTTPException
import numpy as np
from models import CropInput
from ml_models import get_models

router = APIRouter(prefix="", tags=["Predictions"])

@router.post("/predict")
async def predict_crop(data: CropInput):
    crop_model, yield_model, price_model, scaler, label_encoder, crop_data = get_models()
    
    input_data = [[data.nitrogen, data.phosphorus, data.potassium,
                   data.temperature, data.humidity, data.ph_value, data.rainfall]]
    
    input_scaled = scaler.transform(input_data)
    crop_encoded = crop_model.predict(input_scaled)[0]
    crop_name = label_encoder.inverse_transform([crop_encoded])[0]
    
    crop_proba = crop_model.predict_proba(input_scaled)[0]
    confidence = float(np.max(crop_proba) * 100)
    
    predicted_yield = float(yield_model.predict(input_data)[0])
    predicted_price = float(price_model.predict(input_data)[0])
    revenue = 0.01 * predicted_yield * predicted_price
    
    return {
        "success": True,
        "crop": crop_name,
        "confidence": round(confidence, 2),
        "yield_kg_per_hectare": round(predicted_yield, 2),
        "price_per_quintal": round(predicted_price, 2),
        "estimated_revenue": round(revenue, 2)
    }

@router.post("/predict-top-3")
async def predict_top_crops(data: CropInput):
    crop_model, yield_model, price_model, scaler, label_encoder, crop_data = get_models()
    
    input_data = [[data.nitrogen, data.phosphorus, data.potassium,
                   data.temperature, data.humidity, data.ph_value, data.rainfall]]
    
    input_scaled = scaler.transform(input_data)
    probabilities = crop_model.predict_proba(input_scaled)[0]
    all_indices = probabilities.argsort()[::-1]
    
    results = []
    seen_crops = set()
    
    for idx in all_indices:
        crop_name = label_encoder.inverse_transform([idx])[0]
        if crop_name in seen_crops:
            continue
        seen_crops.add(crop_name)
        
        confidence = float(probabilities[idx] * 100)
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
        
        if len(results) == 3:
            break
    
    return {"success": True, "top_crops": results}