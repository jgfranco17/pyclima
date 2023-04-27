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
        self.__url = f'{self.endpoint}&' + "&".join([f'{key}={value}' for key, value in self.__parameters.items()])

    def __repr__(self) -> str:
        return f'<class Forecaster at {hex(id(self))}, coordinates=({self.__latitude},{self.__longitude})>'
    
    def get_current_weather(self) -> dict:
        """
        Retrieve current weather data from API.

        Returns:
            dict: Compiled weather data
        """
        weather_data = self.retrieve_json(url=self.__url, metric="current_weather")
        weather_data["is_day"] = bool(weather_data.get("is_day"))
        weather_data["time"] = dt.datetime.strptime(weather_data.get("time"), "%Y-%m-%dT%H:%M")
        
        return weather_data

    def get_historical(self, span:int=7) -> pd.DataFrame:
        """
        Retrieve dataframe of historical weather data.

        Args:
            span (int, optional): Number of historical days, defaults to 7

        Raises:
            ValueError: Raised if span is not an integer from 1 to 92

        Returns:
            pd.DataFrame: Compiled dataframe of weather data
        """
        try:
            if not 0 < span <= 92:
                raise ValueError(f'{span} is not an integer from 1 to 92')
                
            raw_hourly_data = self.retrieve_json(url=self.__url, parameters=f'&past_days={span}', metric="hourly")
            hourly_timestamps = [dt.datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in raw_hourly_data["time"]]
            format_string = lambda s: s.replace("_2m", "")
            hourly_data = {format_string(key): series for key, series in raw_hourly_data.items() if key != "time"}

            return pd.DataFrame(hourly_data, index=hourly_timestamps)
        
        except ValueError as ve:
            print(f'Invalid value provided: {ve}')
            return None
