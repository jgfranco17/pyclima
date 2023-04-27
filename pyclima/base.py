class WeatherTool:
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self, latitude:float, longitude:float):
        self.__latitude, self.__longitude = latitude, longitude

    @property
    def coordinates(self) -> tuple:
        return self.__latitude, self.__longitude