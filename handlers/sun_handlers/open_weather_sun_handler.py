import requests
import datetime

from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler


class OpenWeatherSunHandler(BaseSunsetHandler):
    def __init__(self, city):
        super().__init__(city)
        self.weather_handler = OpenWeatherHandler(city)

    def ping(self):
        return self.weather_handler.ping()

    def get_url(self):
        return self.weather_handler.get_url_current()

    def get_ascii_time(self):
        response = requests.get(self.get_url())
        weather_data = response.json()
        timezone = weather_data["timezone"]

        sunrise = weather_data["sys"]["sunrise"]
        sunset = weather_data["sys"]["sunset"]

        return sunrise, sunset
