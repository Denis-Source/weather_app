import requests
import logging

from handlers.city_handlers.base_city_handler import BaseCityHandler
from handlers.errors import BadCityNameException, NoAPIConnectionException, WeatherAppException, \
    ServiceUnavailableException
from handlers.city import City

from config import Config


class OpenWeatherCityHandler(BaseCityHandler):
    API_NAME = "OpenWeather"

    def __init__(self, name):
        super().__init__(name)
        self.logger = logging.getLogger("ow_city")

    def ping(self):
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("http://api.openweathermap.org", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} weather")
            return False

    def get_url(self):
        url = f"http://api.openweathermap.org/geo/1.0/direct" \
              f"?q={self.name}&" \
              f"limit=1&appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created city url for {self.API_NAME}: {url}")
        return url

    def get_city(self):
        try:
            response = requests.get(self.get_url())

            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            self.logger.info(f"Got current city request from {self.API_NAME}")
            city_dict = response.json()[0]

            return City(
                name=city_dict["name"],
                longitude=city_dict["lon"],
                latitude=city_dict["lat"],
                state=city_dict.get("state")
            )
        except (KeyError, IndexError):
            self.logger.info("Bad city name")
            raise BadCityNameException(self.name)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException({self.API_NAME}, "city_info")
