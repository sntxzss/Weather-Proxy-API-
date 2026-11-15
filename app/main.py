from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.cache import TTLCache
from app.config import settings
from app.routers import weather
from app.services import CityNotFound, UpstreamTimeout

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=settings.timeout)
    app.state.cache = TTLCache(ttl=settings.cache_ttl)
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(CityNotFound)
async def city_not_found_handler(request: Request, exc: CityNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"City not found: {exc.city}"},
    )

@app.exception_handler(UpstreamTimeout)
async def upstream_timeout_handler(request: Request, exc: UpstreamTimeout):
    return JSONResponse(
        status_code=504,
        content={"detail": f"Upstream timed out: {exc.city}"},
    )

app.include_router(weather.router)