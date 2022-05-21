import requests
import logging

from handlers.city_handlers.base_city_handler import BaseCityHandler
from handlers.errors import BadCityNameException, NoAPIConnectionException, WeatherAppException, \
    ServiceUnavailableException
from handlers.city import City


class MetaWeatherCityHandler(BaseCityHandler):
    """
    MetaWeather city handler class
    Does not require API key
    Gets only city geolocation
    url: https://www.metaweather.com/api/
    Attributes:
        logger
    Constants:
        API_NAME       short API name
    """

    API_NAME = "MetaWeather"

    def __init__(self, name):
        super().__init__(name)
        self.logger = logging.getLogger("mw_city")

    def ping(self) -> bool:
        """
        MetaWeather API connection test
        Tries to connect to the API for one second

        :return: whether the call was successful
        """

        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://www.metaweather.com/api/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} weather")
            return False

    def get_url(self) -> str:
        """
        Gets MetaWeather API url to get the information about the location

        :return: URL that can be visited to get the information
        """

        url = f"https://www.metaweather.com/api/location/search/" \
              f"?query={self.name}"
        self.logger.debug(f"Created city url for {self.API_NAME}: {url}")
        return url

    def get_city(self) -> City:
        """
        Gets city information
        :return: city object

        :raises:
            BadCityNameException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """

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
            raise NoAPIConnectionException(self.API_NAME, "city_info")
