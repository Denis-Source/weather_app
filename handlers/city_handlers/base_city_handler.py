from abc import ABC, abstractmethod


class BaseCityHandler(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def get_city(self):
        pass
