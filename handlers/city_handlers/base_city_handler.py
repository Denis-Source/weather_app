from abc import ABC, abstractmethod

from handlers.city import City


class BaseCityHandler(ABC):
    """
    City handler abstract base class
    Attributes:
        name
    Constants:
        API_NAME       short API name
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def ping(self) -> bool:
        """API connection test"""
        pass

    @abstractmethod
    def get_url(self) -> str:
        """API url to get city information"""
        pass

    @abstractmethod
    def get_city(self) -> City:
        """Gets city information return City object instance"""
        pass
