import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Global variables
crop_model = None
yield_model = None
price_model = None
scaler = None
label_encoder = None
crop_data = None

def load_ml_models():
    global crop_model, yield_model, price_model, scaler, label_encoder, crop_data
    
    crop_data = pd.read_excel("Updated_Crop_Yield_Prediction.xlsx")
    print(f"✅ Loaded {len(crop_data)} rows")
    
    X = crop_data[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 
                    'Humidity', 'pH_Value', 'Rainfall']]
    y_crop = crop_data['Crop']
    y_yield = crop_data['Yield']
    y_price = crop_data['Price']
    
    label_encoder = LabelEncoder()
    y_crop_encoded = label_encoder.fit_transform(y_crop)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    crop_model = RandomForestClassifier(n_estimators=100, random_state=42)
    crop_model.fit(X_scaled, y_crop_encoded)
    
    yield_model = RandomForestRegressor(n_estimators=100, random_state=42)
    yield_model.fit(X, y_yield)
    
    price_model = RandomForestRegressor(n_estimators=100, random_state=42)
    price_model.fit(X, y_price)
    
    print("🚀 All models loaded!")

def get_models():
    return crop_model, yield_model, price_model, scaler, label_encoder, crop_data