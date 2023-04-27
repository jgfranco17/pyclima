import requests


class WeatherTool:
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self, latitude:float, longitude:float):
        self.__latitude, self.__longitude = latitude, longitude
        self.__endpoint = f'{self.BASE_URL}/forecast?latitude={latitude}&longitude={longitude}&timezone=auto'

    @property
    def coordinates(self) -> tuple:
        """
        Returns the target coordinates of the current instance.
        """
        return self.__latitude, self.__longitude
    
    @property
    def endpoint(self) -> str:
        return self.__endpoint
    
    def retrieve_json(self, url:str, parameters:str) -> dict:
        """
        Given a base URL and additional parameters, retrieve the
        weather data and parse the JSON into a dict.
        
        Args:
            url (str): Base URL
            parameters (str): Additional parameters for endpoint

        Raises:
            requests.JSONDecodeError: Raised if JSON data fails to parse

        Returns:
            dict: Parsed JSON data
        """
        try:
            data = requests.get(url + parameters)
            return data.json()

        except requests.JSONDecodeError as jde:
            print(f'Failed to decode JSON data: {jde}')
            return None