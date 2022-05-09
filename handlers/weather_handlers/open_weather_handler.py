import requests
import logging

from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather_handlers.weather import Weather
from config import Config


class OpenWeatherHandler(BaseWeatherHandler):
    def __init__(self, longitude, latitude):
        super().__init__(longitude, latitude)
        self.logger = logging.getLogger("ow_wthr")

    STATUS_TABLE = {
        "clear sky": "sunny",
        "few clouds": "cloudy",
        "scattered clouds": "cloudy",
        "overcast clouds": "overcast",
        "broken clouds": "overcast",
        "shower rain": "sunny rain",
        "light rain": "sunny rain",
        "rain": "rain",
        "moderate rain": "rain",
        "heavy intensity rain": "rain",
        "thunderstorm": "rain",
        "snow": "snow",
        "light snow": "snow",
        "moderate snow": "snow",
        "heavy snow": "snow",
        "mist": "mist"
    }

    def ping(self):
        try:
            self.logger.debug("Trying to ping openweather")
            timeout = 1
            requests.get("http://api.openweathermap.org", timeout=timeout)
            self.logger.info("Ping to openweather successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning("Cant ping openweather city")
            return False

    def get_url_current(self):
        url = f"https://api.openweathermap.org/data/2.5/weather" \
               f"?lat={self.latitude}&lon={self.longitude}&" \
               f"appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created current url for openweather: {url}")
        return url

    def get_url_forecast(self):
        url = f"https://api.openweathermap.org/data/2.5/onecall" \
               f"?lat={self.latitude}&lon={self.longitude}" \
               f"&appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created forecast url for openweather: {url}")
        return url

    def get_weather_current(self):
        try:
            response = requests.get(self.get_url_current())
            self.logger.info("Got current weather request from openweather")
            weather_dict = response.json()
            return Weather(
                city_name=weather_dict["name"],
                status=self.STATUS_TABLE[weather_dict["weather"][0]["description"]],
                temperature=weather_dict["main"]["temp"] - 273.15,
                pressure=weather_dict["main"]["pressure"],
                humidity=weather_dict["main"]["humidity"],
                wind_speed=weather_dict["wind"]["speed"],
                wind_direction=weather_dict["wind"]["deg"],
                time=weather_dict["dt"],
                time_zone=weather_dict["timezone"]
            )
        except (KeyError, requests.ConnectionError, requests.Timeout):
            self.logger.warning("Error connecting openweather")

    def get_weather_forecast(self, n):
        try:
            response = requests.get(self.get_url_forecast())
            self.logger.info("Got forecast weather request from openweather")
            results = response.json()
            forecast = []
            for day_info in results["daily"]:
                weather = Weather(
                    city_name=None,
                    status=self.STATUS_TABLE[day_info["weather"][0]["description"]],
                    temperature=day_info["temp"]["day"] - 273.15,
                    pressure=day_info["pressure"],
                    humidity=day_info["humidity"],
                    wind_speed=day_info["wind_speed"],
                    wind_direction=day_info["wind_deg"],
                    time=day_info["dt"],
                    time_zone=results["timezone_offset"]
                )
                forecast.append(weather)
            return forecast[1:n+1]
        except (KeyError, requests.ConnectionError, requests.Timeout):
            self.logger.warning("Error connecting openweather")
