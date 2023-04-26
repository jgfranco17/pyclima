import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


class Forecaster:
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self, latitude:float, longitude:float, span:int=7) -> None:
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
    def url(self) -> str:
        return self.__url

    @property
    def coordinates(self) -> tuple:
        return self.__latitude, self.__longitude
