from typing import List

import requests
import logging
import datetime

from handlers.city import City
from handlers.weather_handlers.base_weather_handler import BaseWeatherHandler
from handlers.weather import Weather
from handlers.errors import NoAPIConnectionException, BadWeatherException, NotCompatibleAPIException

from config import Config


class AccuWeatherHandler(BaseWeatherHandler):
    """
    AccuWeather handler class
    Requires API key
    API key should be set in Config as ACCUWEATHER_API_KEY
    url: https://developer.accuweather.com/
    Attributes:
        city           city object instance
        logger
    Constants:
        API_NAME       short API name
        STATUS_TABLE   Weather object and API weather status mapping
    """
    API_NAME = "AccuWeather"
    STATUS_TABLE = {
        1: Weather.CLEAR,
        2: Weather.CLEAR,
        3: Weather.CLEAR,
        4: Weather.CLOUDY,
        5: Weather.MIST,
        6: Weather.CLOUDY,
        7: Weather.CLOUDY,
        8: Weather.OVERCAST,
        11: Weather.MIST,
        12: Weather.RAIN,
        13: Weather.SUNNY_RAIN,
        14: Weather.SUNNY_RAIN,
        15: Weather.THUNDERSTORM,
        16: Weather.THUNDERSTORM,
        17: Weather.SUNNY_RAIN,
        18: Weather.RAIN,
        19: Weather.STORM,
        20: Weather.CLOUDY,
        21: Weather.CLOUDY,
        22: Weather.SNOW,
        23: Weather.SNOW,
        24: Weather.SNOW,
        25: Weather.SNOW,
        26: Weather.RAIN,
        29: Weather.SNOW,
        30: Weather.CLEAR,
        31: Weather.CLEAR,
        32: Weather.CLEAR,
        33: Weather.CLEAR,
        34: Weather.CLEAR,
        35: Weather.CLEAR,
        36: Weather.CLOUDY,
        37: Weather.MIST,
        38: Weather.CLOUDY,
        39: Weather.RAIN,
        40: Weather.RAIN,
        41: Weather.THUNDERSTORM,
        42: Weather.THUNDERSTORM,
        43: Weather.STORM,
        44: Weather.SNOW
    }

    def __init__(self, city: City):
        super().__init__(city)
        self.logger = logging.getLogger("aw_wthr")

    def ping(self) -> bool:
        """
        AccuWeather API connection test
        Tries to connect to the API for one second

        :return: whether the call was successful
        """

        try:
            self.logger.debug(f"Trying to ping {self.API_NAME}")
            timeout = 1
            requests.get("https://developer.accuweather.com/", timeout=timeout)
            self.logger.info(f"Ping to {self.API_NAME} successful")
            return True
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Cant ping {self.API_NAME} weather")
            return False

    def get_url_current(self) -> str:
        """
        Gets OpenWeather API url to get the current weather
        To have a successful call, AccuWeather API requires city woeid
        if not provided in the City object raises the corresponding message

        :return: URL that can be visited to get a forecast
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """

        if self.city.woeid:
            url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/" \
                  f"{self.city.woeid}?apikey={Config.ACCUWEATHER_API_KEY}" \
                  f"&details=true&metric=true"
            self.logger.debug(f"Created current url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

    def get_url_forecast(self) -> str:
        """
        Gets AccuWeather API url to get a forecast
        To have a successful call, AccuWeather API requires city woeid
        if not provided in the City object, raises the corresponding message

        :return: URL that can be visited to get a forecast
        :raises:
            NotCompatibleAPIException   if the api is not compatible with the city object
        """

        if self.city.woeid:
            url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
                  f"{self.city.woeid}?apikey={Config.ACCUWEATHER_API_KEY}&details=true&metric=true"
            self.logger.debug(f"Created forecast url for {self.API_NAME}: {url}")
            return url
        else:
            self.logger.warning(f"Not compatible {self.API_NAME}")
            raise NotCompatibleAPIException(self.API_NAME)

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
            self.logger.info(f"Got current weather request from {self.API_NAME}")
            weather_dict = response.json()[0]
            date = datetime.datetime.fromisoformat(weather_dict["DateTime"])
            time_zone = date.utcoffset() / datetime.timedelta(seconds=1)
            return Weather(
                location_name=self.city.name,
                status=self.STATUS_TABLE[weather_dict["WeatherIcon"]],
                temperature=weather_dict["Temperature"]["Value"],
                pressure=None,
                humidity=weather_dict["RelativeHumidity"],
                wind_speed=weather_dict["Wind"]["Speed"]["Value"] / 3.6,
                wind_direction=weather_dict["Wind"]["Direction"]["Degrees"],
                time=weather_dict["EpochDateTime"],
                time_zone=time_zone
            )
        except (KeyError, IndexError):
            self.logger.warning(f"Bad weather response {self.API_NAME}")
            raise BadWeatherException(self.API_NAME)
        except (requests.ConnectionError, requests.Timeout):
            self.logger.warning(f"Error connecting {self.API_NAME}")
            raise NoAPIConnectionException(self.API_NAME, "current weather")

    def get_weather_forecast(self, n: int) -> List[Weather]:
        """
        Gets a forecast from the AccuWeather API

        :param n:   number of predicted days

        :return:   Weather object list with the corresponding information

        :raises:
            BadWeatherException             API response is not parsable
            NoAPIConnectionException        API is not accessible
            ServiceUnavailableException     API returned bad a response
        """
        try:
            response = requests.get(self.get_url_forecast())
            self.logger.info(f"Got forecast weather request from {self.API_NAME}")
            results = response.json()
            forecast = []
            for day_info in results["DailyForecasts"]:
                date = datetime.datetime.fromisoformat(day_info["Date"])
                time_zone = date.utcoffset() / datetime.timedelta(seconds=1)
                weather = Weather(
                    location_name=self.city.name,
                    status=self.STATUS_TABLE[day_info["Day"]["Icon"]],
                    temperature=day_info["Temperature"]["Maximum"]["Value"],
                    pressure=None,
                    humidity=None,
                    wind_speed=day_info["Day"]["Wind"]["Speed"]["Value"],
                    wind_direction=day_info["Day"]["Wind"]["Direction"]["Degrees"],
                    time=day_info["EpochDate"],
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
