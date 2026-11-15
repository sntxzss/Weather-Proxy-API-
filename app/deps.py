import httpx
from fastapi import Request
from app.cache import TTLCache

def get_http(request: Request) -> httpx.AsyncClient:
    return request.app.state.http

def get_cache(request: Request) -> TTLCache:
    return request.app.state.cache