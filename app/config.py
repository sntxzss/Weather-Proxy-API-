from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    geocoding_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    forecast_url: str = "https://api.open-meteo.com/v1/forecast"
    timeout: float = 5.0
    cache_ttl: float = 600.0

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")

settings = Settings()
