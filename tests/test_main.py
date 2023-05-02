import pytest
import datetime as dt
from unittest.mock import Mock
from pyclima.models.base import WeatherTool


def test_get_current_weather(forecaster):
    current = forecaster.get_current_weather()
    assert current["temperature"] == 10
    assert current["relativehumidity"] == 60
    assert current["is_day"] == True
    assert str(current["time"]) == "2023-04-25 00:00:00"


def test_get_historical(forecaster):
    historical = forecaster.get_historical(span=2)
    assert len(historical) == 4
    day_entry = historical.index[0]
    assert day_entry.year == 2023
    assert day_entry.month == 4
    assert day_entry.day == 23


def test_invalid_span(forecaster):
    historical = forecaster.get_historical(span=0)
    assert historical is None
    historical = forecaster.get_historical(span=93)
    assert historical is None


def test_invalid_metric(forecaster):
    tool = WeatherTool(latitude=37.7749, longitude=-122.4194)
    tool.retrieve_json = Mock(return_value={"invalid_metric": []})
    forecaster._Forecaster__url = "http://fakeurl.com"
    current = forecaster.get_current_weather()
    assert current is None
    historical = forecaster.get_historical(span=7)
    assert historical is None
