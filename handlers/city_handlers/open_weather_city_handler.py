import requests
import logging

from handlers.city_handlers.base_city_handler import BaseCityHandler
from handlers.city_handlers.city import City

from config import Config


class OpenWeatherCityHandler(BaseCityHandler):
    def __init__(self, ascii_name):
        super().__init__(ascii_name)
        self.logger = logging.getLogger("ow_city")

    def ping(self):
        try:
            self.logger.debug("Trying to ping openweather")
            timeout = 1
            requests.get("http://api.openweathermap.org", timeout=timeout)
            self.logger.info("Ping to openweather successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning("Cant ping openweather weather")
            return False

    def get_url(self):
        url = f"http://api.openweathermap.org/geo/1.0/direct" \
              f"?q={self.city_ascii_name}&" \
              f"limit=1&appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created city url for openweather {url}")
        return url

    def get_city(self):
        try:
            response = requests.get(self.get_url())
            self.logger.info("Got current city request from openweather")
            city_dict = response.json()[0]

            return City(
                name=city_dict["name"],
                longitude=city_dict["lon"],
                latitude=city_dict["lat"],
                state=city_dict.get("state")
            )
        except (KeyError, requests.ConnectionError, requests.Timeout, IndexError):
            self.logger.warning("Error connecting openweather")