from typing import List

import requests
import logging

from handlers.city import City
from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather import Weather
from handlers.errors import NoAPIConnectionException, BadWeatherException, NotCompatibleAPIException, \
    ServiceUnavailableException

from config import Config


class OpenWeatherHandler(BaseWeatherHandler):
    """
    OpenWeather handler class
    Requires API key
    API key should be set in Config as OPEN_WEATHER_API_KEY
    url: https://openweathermap.org/api
    Attributes:
        city           city object instance
        logger
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping
    """
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

    def __init__(self, city: City):
        super().__init__(city)
        self.logger = logging.getLogger("ow_wthr")

    def ping(self) -> bool:
        """
        OpenWeather API connection test
        Tries to connect to the API for one second

        :return: whether the call was successful
        """
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("http://api.openweathermap.org", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} city")
            return False

    def get_url_current(self) -> str:
        """
        Gets OpenWeather API url to get the current weather
        To have as successful call, OpenWeather API requires city longitude and latitude
        if not provided in the City object, raises corresponding message

        :return: URL that can be visited to get the weather information
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """
        if self.city.longitude and self.city.latitude:
            url = f"https://api.openweathermap.org/data/2.5/weather" \
                  f"?lat={self.city.latitude}&lon={self.city.longitude}&" \
                  f"appid={Config.OPEN_WEATHER_API_KEY}"
            self.logger.debug(f"Created current url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

    def get_url_forecast(self):
        """
        Gets OpenWeather API url to get a forecast
        To have a successful call, OpenWeather API requires city longitude and latitude
        if not provided in the City object, raises the corresponding message

        :return: URL that can be visited to get a forecast
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """
        if self.city.longitude and self.city.latitude:
            url = f"https://api.openweathermap.org/data/2.5/onecall" \
                  f"?lat={self.city.latitude}&lon={self.city.longitude}" \
                  f"&appid={Config.OPEN_WEATHER_API_KEY}"
            self.logger.debug(f"Created forecast url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

    def get_weather_current(self) -> Weather:
        """
        Gets the current weather from the OpenWeather API

        :return: Weather object object with the corresponding information

        :raises:
            BadWeatherException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """
        try:
            response = requests.get(self.get_url_current())
            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)
            self.logger.info(f"Got current weather request from {self.API_NAME}")
            weather_dict = response.json()
            return Weather(
                location_name=weather_dict["name"],
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

    def get_weather_forecast(self, n: int) -> List[Weather]:
        """
        Gets a forecast from the OpenWeather API

        :param n:   number of predicted days

        :return:   Weather object list with the corresponding information

        :raises:
            BadWeatherException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """
        try:
            response = requests.get(self.get_url_forecast())
            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            self.logger.info(f"Got forecast weather request from {self.API_NAME}")
            results = response.json()
            forecast = []
            for day_info in results["daily"]:
                weather = Weather(
                    location_name=self.city.name,
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
        except (KeyError, IndexError):
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException
