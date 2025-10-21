from fastapi import APIRouter, HTTPException
from ml_models import get_models

router = APIRouter(prefix="", tags=["Crops"])

@router.get("/crops")
async def get_all_crops():
    """Get list of all available crops"""
    _, _, _, _, _, crop_data = get_models()
    
    crops = crop_data['Crop'].unique().tolist()
    return {
        "success": True,
        "crops": sorted(crops),
        "total": len(crops)
    }

@router.get("/crop-history/{crop_name}")
async def get_crop_history(crop_name: str):
    """Get historical yield/price data for a specific crop"""
    try:
        _, _, _, _, _, crop_data = get_models()
        
        # Case-insensitive search
        crop_history = crop_data[crop_data['Crop'].str.lower() == crop_name.lower()]
        
        if crop_history.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"Crop '{crop_name}' not found in database"
            )
        
        # Prepare historical data
        history_data = []
        for idx, row in crop_history.iterrows():
            history_data.append({
                "index": int(idx),
                "yield": float(row['Yield']),
                "price": float(row['Price']),
                "rainfall": float(row['Rainfall']),
                "temperature": float(row['Temperature'])
            })
        
        # Limit to last 20 records for cleaner charts
        history_data = history_data[-20:] if len(history_data) > 20 else history_data
        
        return {
            "success": True,
            "crop": crop_name.title(),
            "total_records": len(crop_history),
            "history": history_data,
            "avg_yield": float(crop_history['Yield'].mean()),
            "max_yield": float(crop_history['Yield'].max()),
            "min_yield": float(crop_history['Yield'].min()),
            "avg_price": float(crop_history['Price'].mean()),
            "max_price": float(crop_history['Price'].max()),
            "min_price": float(crop_history['Price'].min())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/crop-info/{crop_name}")
async def get_crop_info(crop_name: str):
    """Get summary information about a specific crop"""
    try:
        _, _, _, _, _, crop_data = get_models()
        
        crop_info = crop_data[crop_data['Crop'].str.lower() == crop_name.lower()]
        
        if crop_info.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"Crop '{crop_name}' not found"
            )
        
        return {
            "success": True,
            "crop": crop_name.title(),
            "avg_yield": float(crop_info['Yield'].mean()),
            "avg_price": float(crop_info['Price'].mean()),
            "avg_revenue": float((0.01 * crop_info['Yield'] * crop_info['Price']).mean()),
            "total_records": len(crop_info),
            "optimal_conditions": {
                "nitrogen": float(crop_info['Nitrogen'].mean()),
                "phosphorus": float(crop_info['Phosphorus'].mean()),
                "potassium": float(crop_info['Potassium'].mean()),
                "temperature": float(crop_info['Temperature'].mean()),
                "humidity": float(crop_info['Humidity'].mean()),
                "ph_value": float(crop_info['pH_Value'].mean()),
                "rainfall": float(crop_info['Rainfall'].mean())
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
