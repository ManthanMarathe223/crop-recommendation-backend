from pydantic import BaseModel

class CropInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph_value: float
    rainfall: float

class CropPrediction(BaseModel):
    crop: str
    confidence: float
    yield_kg_per_hectare: float
    price_per_quintal: float
    estimated_revenue: float