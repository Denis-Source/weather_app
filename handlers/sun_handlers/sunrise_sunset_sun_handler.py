import datetime
import logging
import requests

from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler

from handlers.sun_info import SunInfo
from handlers.errors import NoAPIConnectionException, BadCityNameException


class SunriseSunsetSunHandler(BaseSunsetHandler):
    API_NAME = "Sunrise Sunset"

    def __init__(self, city):
        super().__init__(city)
        self.logger = logging.getLogger("sun_ss")

    def ping(self):
        try:
            self.logger.debug("Trying to ping sunrise-sunset")
            timeout = 1
            requests.get("https://sunrise-sunset.org", timeout=timeout)
            self.logger.info("Ping to sunrise-sunset successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning("Cant ping sunrise-sunset city")
            return False

    def get_url(self):
        url = f"https://api.sunrise-sunset.org/json?lat=" \
              f"{self.city.latitude}&lng={self.city.longitude}&formatted=0"
        self.logger.debug(f"Created current url for sunrise-sunset: {url}")
        return url

    def get_sun_info(self):
        try:
            self.logger.debug(f"Getting sun info from {self.API_NAME}")
            response = requests.get(self.get_url())
            sun_data = response.json()

            sunrise = datetime.datetime.fromisoformat(sun_data["results"]["sunrise"])
            sunset = datetime.datetime.fromisoformat(sun_data["results"]["sunset"])
            return SunInfo(sunrise.timestamp(), sunset.timestamp())
        except (requests.ConnectionError, requests.Timeout):
            raise NoAPIConnectionException(self.API_NAME, "sun info")
        except KeyError:
            raise BadCityNameException(self.city.name)
