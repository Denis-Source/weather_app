from abc import ABC, abstractmethod
from handlers.city import City


class BaseWeatherHandler(ABC):
    def __init__(self, city: City):
        self.city = city

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def get_url_current(self):
        pass

    @abstractmethod
    def get_url_forecast(self):
        pass

    @abstractmethod
    def get_weather_current(self):
        pass

    @abstractmethod
    def get_weather_forecast(self, n):
        pass
