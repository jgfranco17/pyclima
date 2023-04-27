import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from .base import WeatherTool


class Forecaster(WeatherTool):    
    def __init__(self, latitude:float, longitude:float) -> None:
        super().__init__(latitude, longitude)
        hourly_metrics = [
            "temperature_2m",
            "apparent_temperature",
            "relativehumidity_2m",
            "dewpoint_2m",
            "rain",
            "showers",
            "visibility",
            "cloudcover"
        ]
        self.__parameters = {
            "hourly": ",".join(hourly_metrics),
            "current_weather": "true"
        }
        self.__url = f'{self.__endpoint}&' + "&".join([f'{key}={value}' for key, value in self.__parameters.items()])

    def __repr__(self) -> str:
        return f'<class Forecaster at {hex(id(self))}, coordinates=({self.__latitude},{self.__longitude})>'
    
    def get_historical(self, span:int=7) -> pd.DataFrame:
        # Get API request response and decode JSON data
        try:
            if not 0 < span <= 92:
                raise ValueError(f'{span} is not an integer from 1 to 92')
                
            weather_data = requests.get(f'{self.__url}&past_days={span}').json()
            raw_hourly_data = weather_data["hourly"]
            hourly_timestamps = [dt.datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in raw_hourly_data["time"]]
            format_string = lambda s: s.replace("_2m", "")
            hourly_data = {format_string(key): series for key, series in raw_hourly_data.items() if key != "time"}

            return pd.DataFrame(hourly_data, index=hourly_timestamps)
            
        except requests.JSONDecodeError as jde:
            print(f'Failed to decode JSON data: {jde}')
            return None
        
        except ValueError as ve:
            print(f'Invalid value provided: {ve}')
            return None
