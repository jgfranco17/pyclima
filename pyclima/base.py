class WeatherTool:
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self, latitude:float, longitude:float):
        self.__latitude, self.__longitude = latitude, longitude
        self.__endpoint = f'{self.BASE_URL}/forecast?latitude={latitude}&longitude={longitude}'

    @property
    def coordinates(self) -> tuple:
        return self.__latitude, self.__longitude
    
    @property
    def endpoint(self) -> str:
        return self.__endpoint