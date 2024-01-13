"""Base class for weather data tooling."""
import requests


class WeatherTool:
    """Weathertool class implements basic functionality for data retrieval."""

    BASE_URL = "https://api.open-meteo.com/v1"

    def __init__(self, latitude: float, longitude: float):
        """Create a WeatherTool instance.

        Args:
            latitude (float): latitude coordinate of target location
            longitude (float): longitude coordinate of target location
        """
        self.__latitude, self.__longitude = latitude, longitude
        self.__endpoint = (
            f"{self.BASE_URL}/forecast?"
            + f"latitude={latitude}&longitude={longitude}&timezone=auto"
        )

    @property
    def coordinates(self) -> tuple:
        """Return the target coordinates of the current instance."""
        return self.__latitude, self.__longitude

    @property
    def endpoint(self) -> str:
        """Get the endpoint string value."""
        return self.__endpoint

    def retrieve_json(
        self, url: str, parameters: str = None, metric: str = None
    ) -> dict:
        """Retrieve weather data and parse the JSON into a dict.

        Args:
            url (str): Base URL
            parameters (str): Additional parameters for endpoint

        Raises:
            requests.JSONDecodeError: Raised if JSON data fails to parse

        Returns:
            dict: Parsed JSON data
        """
        try:
            if metric is None:
                raise ValueError("No valid metric provided.")

            params = parameters if parameters is not None else ""
            data = dict(requests.get(url + params).json())
            return data.get(metric, None)

        except ValueError as ve:
            print(f"Error during JSON retrieval: {ve}")

        except requests.JSONDecodeError as jde:
            print(f"Failed to decode JSON data: {jde}")
            return None
