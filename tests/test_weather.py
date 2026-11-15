from tests.conftest import FakeHttp

GEOCODE_OK = {"results": [{"latitude": 50.45, "longitude": 30.52, "name": "Kyiv"}]}
FORECAST_OK = {"current_weather": {"temperature": 5.0, "windspeed": 10.0}}

def test_get_weather_success(client):
    fake = FakeHttp(geocode_response=GEOCODE_OK, forecast_response=FORECAST_OK)
    client.app.state.http = fake

    response = client.get("/weather/Kyiv")

    assert response.status_code == 200
    assert response.json() == {"city": "Kyiv", "temperature": 5.0, "wind_speed": 10.0}

def test_get_weather_uses_cache(client):
    fake = FakeHttp(geocode_response=GEOCODE_OK, forecast_response=FORECAST_OK)
    client.app.state.http = fake

    client.get("/weather/Kyiv")
    client.get("/weather/kyiv")

    assert fake.calls == 2

def test_city_not_found(client):
    fake = FakeHttp(geocode_response={"results": []}, forecast_response=None)
    client.app.state.http = fake

    response = client.get("/weather/Atlantis")

    assert response.status_code == 404

def test_upstream_timeout(client):
    fake = FakeHttp(raise_timeout=True)
    client.app.state.http = fake

    response = client.get("/weather/Kyiv")

    assert response.status_code == 504