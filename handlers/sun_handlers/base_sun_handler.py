from abc import ABC, abstractmethod


class BaseSunsetHandler(ABC):
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

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
