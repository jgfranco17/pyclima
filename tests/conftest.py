import sys
import pytest


@pytest.fixture(scope="module")
def mock_weather_data():
    yield {
        "city": "New York",
        "temperature": 15,
        "description": "Cloudy",
        "humidity": 60,
        "wind_speed": 10,
        "pressure": 1015
    }
