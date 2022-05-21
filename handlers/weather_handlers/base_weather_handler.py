from abc import ABC, abstractmethod
from typing import List

from handlers.city import City
from handlers.weather import Weather


class BaseWeatherHandler(ABC):
    """
    Weather handler abstract base class
    Attributes:
        city           city object instance
        logger
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping
    """
    API_NAME = None
    STATUS_TABLE = None

    def __init__(self, city: City):
        self.city = city

    @abstractmethod
    def ping(self) -> bool:
        """API connection test"""
        pass

    @abstractmethod
    def get_url_current(self) -> str:
        """API url to get the current weather"""
        pass

    @abstractmethod
    def get_url_forecast(self) -> str:
        """API url to get a weather forecast"""
        pass

    @abstractmethod
    def get_weather_current(self) -> Weather:
        """Gets the current weather from the API"""
        pass

    @abstractmethod
    def get_weather_forecast(self, n: int) -> List[Weather]:
        """Gets a forecast from the API"""
        pass
