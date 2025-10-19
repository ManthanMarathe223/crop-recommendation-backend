import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Language translations
TRANSLATIONS = {
    "en": {
        "nitrogen": "Nitrogen",
        "phosphorus": "Phosphorus",
        "potassium": "Potassium",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "ph_value": "pH Value",
        "rainfall": "Rainfall",
        "crop": "Crop",
        "yield": "Yield",
        "price": "Price",
        "revenue": "Revenue"
    },
    "hi": {
        "nitrogen": "नाइट्रोजन",
        "phosphorus": "फास्फोरस",
        "potassium": "पोटैशियम",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "ph_value": "पीएच मान",
        "rainfall": "वर्षा",
        "crop": "फसल",
        "yield": "उपज",
        "price": "मूल्य",
        "revenue": "राजस्व"
    },
    "mr": {
        "nitrogen": "नायट्रोजन",
        "phosphorus": "फॉस्फरस",
        "potassium": "पोटॅशियम",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "ph_value": "पीएच मूल्य",
        "rainfall": "पाऊस",
        "crop": "पीक",
        "yield": "उत्पन्न",
        "price": "किंमत",
        "revenue": "महसूल"
    }
}

LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "hi", "name": "हिंदी"},
    {"code": "mr", "name": "मराठी"}
]