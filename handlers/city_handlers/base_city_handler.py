from abc import ABC, abstractmethod


class BaseCityHandler(ABC):
    def __init__(self, ascii_name):
        self.city_ascii_name = ascii_name

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def get_city(self):
        pass
