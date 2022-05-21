import datetime
import logging
import requests

from handlers.city import City
from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler

from handlers.sun_info import SunInfo
from handlers.errors import NoAPIConnectionException, BadCityNameException, ServiceUnavailableException


class SunriseSunsetSunHandler(BaseSunsetHandler):
    """
    Gets and return the information about sunrise and sunset timings

    Attributes:
        city           city object instance
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping

    """

    API_NAME = "Sunrise Sunset"

    def __init__(self, city: City):
        super().__init__(city)
        self.logger = logging.getLogger("sun_ss")

    def ping(self) -> bool:
        """
        Sunrise Sunset API connection test
        Tries to connect to the API for one second

        :return: whether the call was successful
        """

        try:
            self.logger.debug("Trying to ping sunrise-sunset")
            timeout = 1
            requests.get("https://sunrise-sunset.org", timeout=timeout)
            self.logger.info("Ping to sunrise-sunset successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning("Cant ping sunrise-sunset city")
            return False

    def get_url(self) -> str:
        """
        Gets Sunrise Sunset API url to get the information about the sun

        :return: URL that can be visited to get the information
        """

        url = f"https://api.sunrise-sunset.org/json?lat=" \
              f"{self.city.latitude}&lng={self.city.longitude}&formatted=0"
        self.logger.debug(f"Created current url for sunrise-sunset: {url}")
        return url

    def get_sun_info(self) -> SunInfo:
        """
        Gets the sun information
        :return: SunInfo object

        :raises:
            BadCityNameException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """

        try:
            self.logger.debug(f"Getting sun info from {self.API_NAME}")
            response = requests.get(self.get_url())
            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            sun_data = response.json()

            sunrise = datetime.datetime.fromisoformat(sun_data["results"]["sunrise"])
            sunset = datetime.datetime.fromisoformat(sun_data["results"]["sunset"])
            return SunInfo(sunrise.timestamp(), sunset.timestamp())
        except (KeyError, IndexError):
            raise BadCityNameException(self.city.name)
        except (requests.ConnectionError, requests.Timeout):
            raise NoAPIConnectionException(self.API_NAME, "sun info")
