import requests

from handlers.city import City
from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler

from handlers.sun_info import SunInfo
from handlers.errors import NoAPIConnectionException, BadCityNameException, ServiceUnavailableException


class OpenWeatherSunHandler(BaseSunsetHandler):
    """
    Gets and return the information about sunrise and sunset timings
    Entirely based on OpenWeatherHandler
    Attributes:
        city           city object instance
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping

    """
    API_NAME = "OpenWeather"

    def __init__(self, city: City):
        super().__init__(city)
        self.weather_handler = OpenWeatherHandler(city)

    def ping(self):
        """Tests connection to the API"""
        return self.weather_handler.ping()

    def get_url(self):
        """Gets a url to the API"""
        return self.weather_handler.get_url_current()

    def get_sun_info(self):
        """
        Gets the sun information from the OpenWeather API

        :return:   Weather object list with the corresponding information

        :raises:
            BadCityNameException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """

        try:
            response = requests.get(self.get_url())
            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            weather_data = response.json()

            sunrise = weather_data["sys"]["sunrise"]
            sunset = weather_data["sys"]["sunset"]
            return SunInfo(sunrise, sunset)
        except (KeyError, IndexError):
            raise BadCityNameException(self.city.name)
        except (requests.ConnectionError, requests.Timeout):
            raise NoAPIConnectionException(self.API_NAME, "sun info")
