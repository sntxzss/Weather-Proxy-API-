from pydantic import BaseModel

class WeatherResponce(BaseModel):
    city: str
    temperature: float
    wind_speed: float
    