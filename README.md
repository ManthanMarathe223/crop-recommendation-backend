# 🌾 Crop Recommendation Backend API

<div align="center">

**[📋 Overview](#-overview)** • 
**[🚀 Features](#-features)** • 
**[📁 Structure](#-project-structure)** • 
**[🛠️ Tech Stack](#️-tech-stack)** • 
**[📊 ML Models](#-machine-learning-models)** • 
**[🌐 API Endpoints](#-api-endpoints)** • 
**[🔧 Installation](#-installation--setup)** • 
**[🚀 Deployment](#-deployment)** 

• 
**[🧪 Testing](#-testing)** • 
**[👥 Team](#-team)** • 
**[🔗 Links](#-related-links)**

---

</div>

## 📋 Overview

This is the backend API for the **Indra Dhanu** Crop Recommendation System, built for climate-resilient agriculture. The system uses Machine Learning to predict optimal crops based on soil and climate parameters.

**Built with:** FastAPI, Scikit-learn, Pandas, ReportLab

---

## 🚀 Features

- ✅ **ML-Powered Predictions** - Recommends top 3 crops with confidence scores
- ✅ **Weather Integration** - Real-time weather data auto-fill
- ✅ **Multi-language Support** - English, Hindi, Marathi translations
- ✅ **PDF Report Generation** - Downloadable crop recommendation reports
- ✅ **Historical Analysis** - Visualize past yield and price trends
- ✅ **RESTful API** - Clean, documented endpoints

---

## 📁 Project Structure

```
crop-recommendation-backend/
├── main.py                          # Main FastAPI application
├── models.py                        # Pydantic request/response models
├── config.py                        # Configuration & translations
├── ml_models.py                     # ML model loading & training
├── routers/
│   ├── __init__.py
│   ├── predictions.py               # Crop prediction endpoints
│   ├── weather.py                   # Weather API integration
│   ├── translations.py              # Language translation endpoints
│   ├── reports.py                   # PDF generation endpoint
│   └── crops.py                     # Crop data & history endpoints
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (not in repo)
├── .gitignore                       # Git ignore rules
└── Updated_Crop_Yield_Prediction.xlsx  # Training dataset
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework for building APIs |
| **Scikit-learn** | Machine Learning (RandomForest models) |
| **Pandas** | Data processing & manipulation |
| **ReportLab** | PDF report generation |
| **OpenWeatherMap API** | Real-time weather data |
| **Python-dotenv** | Environment variable management |

---

## 📊 Machine Learning Models

### 1. **Crop Classification Model**
- **Algorithm:** Random Forest Classifier
- **Purpose:** Predicts best-suited crop
- **Input:** 7 soil/climate parameters
- **Output:** Crop name + confidence score

### 2. **Yield Prediction Model**
- **Algorithm:** Random Forest Regressor
- **Purpose:** Estimates crop yield (kg/hectare)
- **Input:** Same 7 parameters
- **Output:** Expected yield

### 3. **Price Prediction Model**
- **Algorithm:** Random Forest Regressor
- **Purpose:** Predicts market price (₹/quintal)
- **Input:** Same 7 parameters
- **Output:** Expected selling price

**Training Data:** 150+ records from `Updated_Crop_Yield_Prediction.xlsx`

---

## 🌐 API Endpoints

### **Health Check**
```
GET /
```
Returns API status and available endpoints.

**Response:**
```json
{
  "message": "🌾 Crop Recommendation API v2.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### **Predictions**

#### 1. Single Crop Prediction
```
POST /api/predict
```

**Request Body:**
```json
{
  "nitrogen": 40,
  "phosphorus": 50,
  "potassium": 60,
  "temperature": 33,
  "humidity": 60,
  "ph_value": 7,
  "rainfall": 200
}
```

**Response:**
```json
{
  "success": true,
  "crop": "Rice",
  "confidence": 85.5,
  "yield_kg_per_hectare": 2500.0,
  "price_per_quintal": 1800.0,
  "estimated_revenue": 45000.0
}
```

---

#### 2. Top 3 Crop Recommendations
```
POST /api/predict-top-3
```

**Request Body:** Same as above

**Response:**
```json
{
  "success": true,
  "top_crops": [
    {
      "crop": "Coffee",
      "confidence": 30.0,
      "yield_kg_per_hectare": 2683.89,
      "price_per_quintal": 2786.34,
      "estimated_revenue": 74782.39
    },
    {
      "crop": "Coconut",
      "confidence": 25.0,
      "yield_kg_per_hectare": 3800.0,
      "price_per_quintal": 2500.0,
      "estimated_revenue": 95000.0
    },
    {
      "crop": "Rice",
      "confidence": 20.0,
      "yield_kg_per_hectare": 2200.0,
      "price_per_quintal": 1600.0,
      "estimated_revenue": 35200.0
    }
  ]
}
```

---

### **Weather Integration**

#### Get Weather Data
```
GET /api/weather/{city}
```

**Example:** `GET /api/weather/Pune`

**Response:**
```json
{
  "success": true,
  "temperature": 28.5,
  "humidity": 65.0,
  "rainfall": 0,
  "city": "Pune"
}
```

**Note:** Uses OpenWeatherMap API. Requires API key in `.env` file.

---

### **Translations**

#### Get Translations
```
GET /api/translations/{lang}
```

**Supported Languages:** `en` (English), `hi` (Hindi), `mr` (Marathi)

**Example:** `GET /api/translations/hi`

**Response:**
```json
{
  "success": true,
  "language": "hi",
  "translations": {
    "nitrogen": "नाइट्रोजन",
    "phosphorus": "फास्फोरस",
    "temperature": "तापमान",
    ...
  }
}
```

---

#### Get Available Languages
```
GET /api/languages
```

**Response:**
```json
{
  "success": true,
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "hi", "name": "हिंदी"},
    {"code": "mr", "name": "मराठी"}
  ]
}
```

---

### **Reports**

#### Generate PDF Report
```
POST /api/generate-report
```

**Request Body:** Same as `/predict`

**Response:** Downloads a PDF file with:
- Soil parameters table
- Top 3 crop recommendations
- Yield, price, and revenue estimates
- Timestamp and branding

**File Name:** `crop_report_YYYYMMDD_HHMMSS.pdf`

---

### **Crop Data**

#### Get All Crops
```
GET /api/crops
```

**Response:**
```json
{
  "success": true,
  "crops": ["Coconut", "Coffee", "Cotton", "Rice", "Wheat", ...],
  "total": 22
}
```

---

#### Get Crop History
```
GET /api/crop-history/{crop_name}
```

**Example:** `GET /api/crop-history/coconut`

**Response:**
```json
{
  "success": true,
  "crop": "Coconut",
  "total_records": 15,
  "history": [
    {
      "index": 0,
      "yield": 2683.89,
      "price": 2786.34,
      "rainfall": 200.0,
      "temperature": 30.5
    },
    ...
  ],
  "avg_yield": 2800.0,
  "max_yield": 3200.0,
  "min_yield": 2400.0,
  "avg_price": 2500.0,
  "max_price": 2800.0,
  "min_price": 2200.0
}
```

**Note:** Returns last 20 records for chart visualization.

---

#### Get Crop Info
```
GET /api/crop-info/{crop_name}
```

**Example:** `GET /api/crop-info/rice`

**Response:**
```json
{
  "success": true,
  "crop": "Rice",
  "avg_yield": 2200.0,
  "avg_price": 1600.0,
  "avg_revenue": 35200.0,
  "total_records": 12,
  "optimal_conditions": {
    "nitrogen": 80,
    "phosphorus": 40,
    "potassium": 40,
    "temperature": 25,
    "humidity": 80,
    "ph_value": 6.5,
    "rainfall": 1500
  }
}
```

---

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/crop-recommendation-backend.git
cd crop-recommendation-backend
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Create `.env` File**
```bash
# Create .env file in root directory
OPENWEATHER_API_KEY=your_api_key_here
```

Get free API key from: [OpenWeatherMap](https://openweathermap.org/api)

### **Step 5: Run Server**
```bash
uvicorn main:app --reload
```

**Server runs at:** `http://localhost:8000`

**API Docs:** `http://localhost:8000/docs` (Interactive Swagger UI)

---

## 📦 Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
scikit-learn==1.3.2
openpyxl==3.1.2
python-multipart==0.0.6
python-dotenv==1.0.0
requests==2.31.0
reportlab==4.0.7
```

---

## 🚀 Deployment

### **Render.com (Recommended)**

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENWEATHER_API_KEY`
6. Deploy!

**Live URL Example:** `https://crop-recommendation-api.onrender.com`

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes |

**Note:** Never commit `.env` file to GitHub!

---

## 📖 API Documentation

Interactive API documentation available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🧪 Testing

### **Test Single Prediction**
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 40,
    "phosphorus": 50,
    "potassium": 60,
    "temperature": 33,
    "humidity": 60,
    "ph_value": 7,
    "rainfall": 200
  }'
```

### **Test Weather API**
```bash
curl "http://localhost:8000/api/weather/Pune"
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Team

**Indra Dhanu Hackathon 2025 - Team**

- **Backend Developer:** [Manthan Marathe](https://github.com/ManthanMarathe223)
- **Frontend Developer:** [Vrushab Hirap](https://github.com/VrushabhHirapOfficial)
  
---

## 🙏 Acknowledgments

- **Hackathon:** Indra Dhanu 2025
- **Theme:** Smart & Climate-Resilient Agriculture
- **Institution:** Pimpri Chinchwad College of Engineering Pune (PCCOE)

---

## 📧 Contact

For questions or support, reach out to: marathemanthanofficial@gmail.com

---

## 🔗 Related Links

- **Frontend Repository:** [GitHub Link](https://github.com/VrushabhHirapOfficial/crop-recommendation-frontend)
- **Live Demo:** [Vercel URL](http://indradhanu.vercel.app)
- **API Documentation:** [Render URL/docs](https://crop-recommendation-api-vudg.onrender.com/docs)

---

**Made with ❤️ for sustainable farming and climate-resilient agriculture** 🌾
