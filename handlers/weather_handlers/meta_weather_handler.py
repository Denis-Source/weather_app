import requests
import logging
import datetime

from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather import Weather
from handlers.errors import NoAPIConnectionException, BadWeatherException, NotCompatibleAPIException

from config import Config


class MetaWeatherHandler(BaseWeatherHandler):
    STATUS_TABLE = {
        "Snow": Weather.SNOW,
        "Sleet": Weather.SNOW,
        "Hail": Weather.SNOW,
        "Thunderstorm": Weather.THUNDERSTORM,
        "Heavy Rain": Weather.RAIN,
        "Light Rain": Weather.RAIN,
        "Showers": Weather.SUNNY_RAIN,
        "Heavy Cloud": Weather.OVERCAST,
        "Light Cloud": Weather.CLOUDY,
        "Clear": Weather.CLEAR
    }

    API_NAME = "MetaWeather"

    def __init__(self, city):
        super().__init__(city)
        self.logger = logging.getLogger("mw_wthr")

    def ping(self):
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://www.metaweather.com/api/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} city")
            return False

    def get_url_current(self):
        if self.city.woeid:
            url = f"https://www.metaweather.com/api/location/" \
                  f"{self.city.woeid}/"
            self.logger.debug(f"Created current url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

    def get_url_forecast(self):
        self.logger.debug("Creating forecast url (calling current url)")
        return self.get_url_current()

    def get_weather_current(self):
        try:
            response = requests.get(self.get_url_current())
            self.logger.info(f"Got current weather request from {self.API_NAME}")
            weather_dict = response.json()

            date = datetime.datetime.fromisoformat(weather_dict["time"])
            time_zone = date.utcoffset() / datetime.timedelta(seconds=1)

            return Weather(
                city_name=self.city.name,
                status=self.STATUS_TABLE[weather_dict["consolidated_weather"][0]["weather_state_name"]],
                temperature=weather_dict["consolidated_weather"][0]["the_temp"],
                pressure=weather_dict["consolidated_weather"][0]["air_pressure"],
                humidity=weather_dict["consolidated_weather"][0]["humidity"],
                wind_speed=weather_dict["consolidated_weather"][0]["wind_speed"],
                wind_direction=weather_dict["consolidated_weather"][0]["wind_direction"],
                time=date.timestamp(),
                time_zone=time_zone
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

            date = datetime.datetime.fromisoformat(results["time"])
            time_zone = date.utcoffset() / datetime.timedelta(seconds=1)

            for day_info in results["consolidated_weather"]:
                date = datetime.datetime.fromisoformat(day_info["applicable_date"])

                weather = Weather(
                    city_name=self.city.name,
                    status=self.STATUS_TABLE[day_info["weather_state_name"]],
                    temperature=day_info["the_temp"],
                    pressure=day_info["air_pressure"],
                    humidity=day_info["humidity"],
                    wind_speed=day_info["wind_speed"],
                    wind_direction=day_info["wind_direction"],
                    time=date.timestamp(),
                    time_zone=time_zone
                )
                forecast.append(weather)
            return forecast[1:n + 1]
        except KeyError:
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException
