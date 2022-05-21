from typing import List

import requests
import logging
import datetime

from handlers.city import City
from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather import Weather
from handlers.errors import NoAPIConnectionException, BadWeatherException, NotCompatibleAPIException, \
    ServiceUnavailableException


class MetaWeatherHandler(BaseWeatherHandler):
    """
    MetaWeather handler class
    Does not requires API key
    url: https://www.metaweather.com/api/
    Attributes:
        city           city object instance
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping
    """

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

    def __init__(self, city: City):
        super().__init__(city)
        self.logger = logging.getLogger("mw_wthr")

    def ping(self) -> bool:
        """
        MetaWeather API connection test
        Tries the connection for one second

        :return: whether the call was successful
        """
        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://www.metaweather.com/api/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} city")
            return False

    def get_url_current(self) -> str:
        """
        Gets MetaWeather API url to get the current weather
        To have a successful call, AccuWeather API requires city woeid
        if not provided in the City object raises the corresponding message

        :return: URL that can be visited to get a forecast
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """

        if self.city.woeid:
            url = f"https://www.metaweather.com/api/location/" \
                  f"{self.city.woeid}/"
            self.logger.debug(f"Created current url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

    def get_url_forecast(self) -> str:
        """
        Gets OpenWeather API url to get a forecast
        To have a successful call, AccuWeather API requires city woeid
        if not provided in the City object, raises the corresponding message
        The url for the current weather and a forecast is the same

        :return: URL that can be visited to get a forecast
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """

        self.logger.debug("Creating forecast url (calling current url)")
        return self.get_url_current()

    def get_weather_current(self) -> Weather:
        """
        Gets the current weather from the AccuWeather API

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

            date = datetime.datetime.fromisoformat(weather_dict["time"])
            time_zone = date.utcoffset() / datetime.timedelta(seconds=1)

            return Weather(
                location_name=self.city.name,
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

    def get_weather_forecast(self, n: int) -> List[Weather]:
        """
        Gets a forecast from the MetaWeather API

        :param n:   number of predicted days

        :return:   Weather object list with the corresponding information

        :raises:
            BadWeatherException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned a bad response
        """

        try:
            response = requests.get(self.get_url_forecast())
            if response.status_code >= 400:
                raise ServiceUnavailableException(self.API_NAME)

            self.logger.info(f"Got forecast weather request from {self.API_NAME}")
            results = response.json()
            forecast = []

            date = datetime.datetime.fromisoformat(results["time"])
            time_zone = date.utcoffset() / datetime.timedelta(seconds=1)

            for day_info in results["consolidated_weather"]:
                date = datetime.datetime.fromisoformat(day_info["applicable_date"])

                weather = Weather(
                    location_name=self.city.name,
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
        except (KeyError, IndexError):
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException
