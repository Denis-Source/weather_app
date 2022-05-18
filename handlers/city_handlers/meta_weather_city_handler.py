import requests
import logging

from handlers.city_handlers.base_city_handler import BaseCityHandler
from handlers.errors import BadCityNameException, NoAPIConnectionException, WeatherAppException, \
    ServiceUnavailableException
from handlers.city import City


class MetaWeatherCityHandler(BaseCityHandler):
    API_NAME = "MetaWeather"

    def __init__(self, name):
        super().__init__(name)
        self.logger = logging.getLogger("mw_city")

    def ping(self):
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://www.metaweather.com/api/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} weather")
            return False

    def get_url(self):
        url = f"https://www.metaweather.com/api/location/search/" \
              f"?query={self.name}"
        self.logger.debug(f"Created city url for {self.API_NAME}: {url}")
        return url

    def get_city(self):
        try:
            response = requests.get(self.get_url())

            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            self.logger.info(f"Got current city request from {self.API_NAME}")
            city_dict = response.json()[0]

            latitude = float(city_dict["latt_long"].split(",")[0])
            longitude = float(city_dict["latt_long"].split(",")[1])

            return City(
                name=city_dict["title"],
                longitude=longitude,
                latitude=latitude,
                woeid=city_dict["woeid"]
            )
        except (KeyError, IndexError, ValueError):
            self.logger.info("Bad city name")
            raise BadCityNameException(self.name)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException({self.API_NAME}, "city_info")