from fastapi import APIRouter, HTTPException
from config import TRANSLATIONS, LANGUAGES

router = APIRouter(prefix="", tags=["Translations"])

@router.get("/translations/{lang}")
async def get_translations(lang: str):
    if lang not in TRANSLATIONS:
        raise HTTPException(status_code=404, detail="Language not supported")
    return {"success": True, "language": lang, "translations": TRANSLATIONS[lang]}

@router.get("/languages")
async def get_languages():
    return {"success": True, "languages": LANGUAGES}