import requests
import logging

from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather import Weather
from handlers.errors import NoAPIConnectionException, BadWeatherException

from config import Config


class OpenWeatherHandler(BaseWeatherHandler):
    STATUS_TABLE = {
        "Thunderstorm": Weather.THUNDERSTORM,
        "Drizzle": Weather.SUNNY_RAIN,
        "Rain": Weather.RAIN,
        "Snow": Weather.SNOW,
        "Mist": Weather.MIST,
        "Smoke": Weather.MIST,
        "Haze": Weather.MIST,
        "Dust": Weather.SANDSTORM,
        "Fog": Weather.MIST,
        "Sand": Weather.SANDSTORM,
        "Ash": Weather.ERUPTION,
        "Squall": Weather.THUNDERSTORM,
        "Tornado": Weather.THUNDERSTORM,
        "Clear": Weather.CLEAR,
        "Clouds": Weather.CLOUDY
    }
    API_NAME = "OpenWeather"

    def __init__(self, longitude, latitude):
        super().__init__(longitude, latitude)
        self.logger = logging.getLogger("ow_wthr")

    def ping(self):
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("http://api.openweathermap.org", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} city")
            return False

    def get_url_current(self):
        url = f"https://api.openweathermap.org/data/2.5/weather" \
              f"?lat={self.latitude}&lon={self.longitude}&" \
              f"appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created current url for {self.API_NAME}: {url}")
        return url

    def get_url_forecast(self):
        url = f"https://api.openweathermap.org/data/2.5/onecall" \
              f"?lat={self.latitude}&lon={self.longitude}" \
              f"&appid={Config.OPEN_WEATHER_API_KEY}"
        self.logger.debug(f"Created forecast url for {self.API_NAME}: {url}")
        return url

    def get_weather_current(self):
        try:
            response = requests.get(self.get_url_current())
            self.logger.info(f"Got current weather request from {self.API_NAME}")
            weather_dict = response.json()
            return Weather(
                city_name=weather_dict["name"],
                status=self.STATUS_TABLE[weather_dict["weather"][0]["main"]],
                temperature=weather_dict["main"]["temp"] - 273.15,
                pressure=weather_dict["main"]["pressure"],
                humidity=weather_dict["main"]["humidity"],
                wind_speed=weather_dict["wind"]["speed"],
                wind_direction=weather_dict["wind"]["deg"],
                time=weather_dict["dt"],
                time_zone=weather_dict["timezone"]
        )
        except KeyError:
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException(self.API_NAME, "current weather")

    def get_weather_forecast(self, n):
        try:
            response = requests.get(self.get_url_forecast())
            self.logger.info(f"Got forecast weather request from {self.API_NAME}")
            results = response.json()
            forecast = []
            for day_info in results["daily"]:
                weather = Weather(
                    city_name=None,
                    status=self.STATUS_TABLE[day_info["weather"][0]["main"]],
                    temperature=day_info["temp"]["day"] - 273.15,
                    pressure=day_info["pressure"],
                    humidity=day_info["humidity"],
                    wind_speed=day_info["wind_speed"],
                    wind_direction=day_info["wind_deg"],
                    time=day_info["dt"],
                    time_zone=results["timezone_offset"]
                )
                forecast.append(weather)
            return forecast[1:n + 1]
        except KeyError:
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
