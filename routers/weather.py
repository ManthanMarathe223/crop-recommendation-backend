from fastapi import APIRouter, HTTPException
import requests
from config import OPENWEATHER_API_KEY

router = APIRouter(prefix="/api", tags=["Weather"])

@router.get("/weather/{city}")
async def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    return {
        "success": True,
        "temperature": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "rainfall": data.get('rain', {}).get('1h', 0),
        "city": city
    }