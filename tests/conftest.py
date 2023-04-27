import pytest
from unittest.mock import Mock
from pyclima.base import WeatherTool
from pyclima.forecast import Forecaster


@pytest.fixture(scope="module")
def forecaster():
    # Use mock objects to avoid hitting the API endpoint
    tool = WeatherTool(latitude=37.7749, longitude=-122.4194)
    tool.retrieve_json = Mock(return_value={
        "temperature_2m": [10, 12, 14, 16],
        "relativehumidity_2m": [60, 65, 70, 75],
        "time": ["2023-04-25T00:00", "2023-04-25T03:00", "2023-04-25T06:00", "2023-04-25T09:00"]
    })
    return Forecaster(latitude=37.7749, longitude=-122.4194)
