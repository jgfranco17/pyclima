import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


class Forecaster:
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self, latitude:float, longitude:float) -> None:
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
        self.__latitude, self.__longitude = latitude, longitude
        self.__endpoint = f'{self.BASE_URL}/forecast?latitude={latitude}&longitude={longitude}'
        self.__parameters = {
            "hourly": ",".join(hourly_metrics),
            "current_weather": "true"
        }
        self.__url = f'{self.__endpoint}&' + "&".join(f'{key}={value}' for key, value in self.__parameters.items())

    def __repr__(self) -> str:
        return f'<class Forecaster at {hex(id(self))}, coordinates=({self.__latitude},{self.__longitude})>'

    @property
    def coordinates(self) -> tuple:
        return self.__latitude, self.__longitude
    
    def get_historical(self, span:int=7) -> pd.DataFrame:
        # Get API request response and decode JSON data
        try:
            weather_data = requests.get(f'{self.__url}&past_days={span}').json()
            raw_hourly_data = weather_data["hourly"]

            # Preparing JSON data for dataframe conversion
            hourly_timestamps = [dt.datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in raw_hourly_data["time"]]
            format_string = lambda s: s.replace("_2m", "")
            hourly_data = {format_string(key): series for key, series in raw_hourly_data.items() if key != "time"}

            # Convert data to dataframe
            df = pd.DataFrame(hourly_data, index=hourly_timestamps)
            
        except requests.JSONDecodeError as jde:
            print(f'Failed to decode JSON data: {jde}')
            return None
