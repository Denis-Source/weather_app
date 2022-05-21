from abc import ABC, abstractmethod
from handlers.city import City


class BaseSunsetHandler(ABC):
    """
    Sunset handler abstract base class
    Attributes:
        city           city object instance
    Constants:
        API_NAME       short API name
    """

    def __init__(self, city: City):
        self.city = city

    @abstractmethod
    def ping(self):
        """API connection test"""
        pass

    @abstractmethod
    def get_url(self):
        """API url to get the sun information"""
        pass

    @abstractmethod
    def get_sun_info(self):
        """Gets the sun information from the API"""
        pass
