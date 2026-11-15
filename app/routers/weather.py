import httpx
from fastapi import APIRouter, Depends

from app.cache import TTLCache
from app.deps import get_cache, get_http
from app.schemas import WeatherResponse
from app.services import get_weather

router = APIRouter()

@router.get("/weather/{city}", response_model=WeatherResponse)
async def read_weather(
    city: str,
    http: httpx.AsyncClient = Depends(get_http),
    cache: TTLCache = Depends(get_cache),
) -> WeatherResponse:
    return await get_weather(http, cache, city)