import requests
import logging

from handlers.city_handlers.base_city_handler import BaseCityHandler
from handlers.errors import BadCityNameException, NoAPIConnectionException, ServiceUnavailableException
from handlers.city import City

from config import Config


class AccuWeatherCityHandler(BaseCityHandler):
    API_NAME = "AccuWeather"

    def __init__(self, name):
        super().__init__(name)
        self.logger = logging.getLogger("aw_city")

    def ping(self):
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://developer.accuweather.com/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} city")
            return False

    def get_url(self):
        url = f"https://dataservice.accuweather.com/locations/v1/cities/autocomplete" \
              f"?apikey={Config.ACCUWEATHER_API_KEY}" \
              f"&q={self.name}"
        self.logger.debug(f"Created city url for {self.API_NAME}: {url}")
        return url

    def get_url_location(self, city):
        url = f"http://dataservice.accuweather.com/locations/v1/" \
              f"{city.woeid}" \
              f"?apikey={Config.ACCUWEATHER_API_KEY}"
        self.logger.debug(f"Created city location url for {self.API_NAME}: {url}")
        return url

    def get_city(self):
        try:
            response = requests.get(self.get_url())
            self.logger.info(f"Got current city request from {self.API_NAME}")
            if response.status_code == 503:
                raise ServiceUnavailableException(self.API_NAME)
            city_dict = response.json()
            city = City(
                name=city_dict["LocalizedName"],
                woeid=city_dict["Key"],
                state=city_dict["Country"]["LocalizedName"]
            )
            response = requests.get(self.get_url_location(city))
            city_dict = response.json()
            city.latitude = city_dict["GeoPosition"]["Latitude"]
            city.longitude = city_dict["GeoPosition"]["Longitude"]

            return city
        except (KeyError, IndexError):
            self.logger.info("Bad city name")
            raise BadCityNameException(self.name)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException({self.API_NAME}, "city_info")
