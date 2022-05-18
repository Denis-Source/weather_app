import requests

from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler

from handlers.sun_info import SunInfo
from handlers.errors import NoAPIConnectionException, BadCityNameException, ServiceUnavailableException


class OpenWeatherSunHandler(BaseSunsetHandler):
    API_NAME = "OpenWeather"

    def __init__(self, city):
        super().__init__(city)
        self.weather_handler = OpenWeatherHandler(city)

    def ping(self):
        return self.weather_handler.ping()

    def get_url(self):
        return self.weather_handler.get_url_current()

    def get_sun_info(self):
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
