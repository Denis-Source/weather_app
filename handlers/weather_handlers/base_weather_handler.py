from abc import ABC, abstractmethod


class BaseWeatherHandler(ABC):
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

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
