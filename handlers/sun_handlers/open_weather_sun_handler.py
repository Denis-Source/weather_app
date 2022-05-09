import requests
import datetime

from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler


class OpenWeatherSunsetHandler(BaseSunsetHandler):
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

        sunrise = weather_data["sys"]["sunrise"] + timezone
        sunset = weather_data["sys"]["sunset"] + timezone

        return sunrise, sunset

    def get_human_time(self):
        sunrise, sunset = self.get_ascii_time()
        sunrise = datetime.datetime.utcfromtimestamp(sunrise)
        sunset = datetime.datetime.utcfromtimestamp(sunset)

        return f"{sunrise.hour}:{sunrise.minute}", f"{sunset.hour}:{sunset.minute}"
