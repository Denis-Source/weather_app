from abc import ABC, abstractmethod
from handlers.city import City


class BaseSunsetHandler(ABC):
    def __init__(self, city: City):
        self.city = city

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_ascii_time(self):
        pass

    def get_human_time(self):
        pass
