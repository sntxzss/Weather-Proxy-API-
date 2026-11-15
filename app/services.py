import httpx
from app.cache import TTLCache
from app.config import settings
from app.schemas import WeatherResponse

class CityNotFound(Exception):
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"City not found: {city}")

class UpstreamTimeout(Exception):
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"Upstream timeout while fetching: {city}")

async def _geocode(http: httpx.AsyncClient, city: str) -> tuple[float, float, str]:
    try:
        response = await http.get(
            settings.geocoding_url,
            params={"name": city, "count": 1},
        )
    except httpx.TimeoutException:
        raise UpstreamTimeout(city)

    data = response.json()
    results = data.get("results")
    if not results:
        raise CityNotFound(city)

    first = results[0]
    return first["latitude"], first["longitude"], first["name"]

async def _fetch_forecast(
    http: httpx.AsyncClient, latitude: float, longitude: float
) -> dict:
    try:
        response = await http.get(
            settings.forecast_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
            },
        )
    except httpx.TimeoutException:
        raise UpstreamTimeout(f"{latitude},{longitude}")

    return response.json()

async def get_weather(
    http: httpx.AsyncClient, cache: TTLCache, city: str
) -> WeatherResponse:
    cached = cache.get(city)
    if cached is not None:
        return cached

    latitude, longitude, canonical_name = await _geocode(http, city)
    forecast = await _fetch_forecast(http, latitude, longitude)

    current = forecast["current_weather"]
    result = WeatherResponse(
        city=canonical_name,
        temperature=current["temperature"],
        wind_speed=current["windspeed"],
    )

    cache.set(city, result)
    return result

    