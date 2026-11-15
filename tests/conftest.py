import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import app

class FakeHttp:
    def __init__(self, geocode_response=None, forecast_response=None, raise_timeout=False):
        self.geocode_response = geocode_response
        self.forecast_response = forecast_response
        self.raise_timeout = raise_timeout
        self.calls = 0

    async def get(self, url, params=None):
        self.calls += 1
        if self.raise_timeout:
            raise httpx.TimeoutException("timed out")

        class Resp:
            def __init__(self_inner, data):
                self_inner._data = data

            def json(self_inner):
                return self_inner._data

        if "geocoding" in url:
            return Resp(self.geocode_response)
        return Resp(self.forecast_response)

    async def aclose(self):
        pass

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client