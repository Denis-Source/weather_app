import datetime
import logging
import requests

from handlers.sun_handlers.base_sun_handler import BaseSunsetHandler


class SunriseSunsetSunHandler(BaseSunsetHandler):
    def __init__(self, longitude, latitude):
        super().__init__(longitude, latitude)
        self.logger = logging.getLogger("sun_ss")

    def ping(self):
        try:
            self.logger.debug("Trying to ping sunrise-sunset")
            timeout = 1
            requests.get("https://sunrise-sunset.org", timeout=timeout)
            self.logger.info("Ping to sunrise-sunset successful")
            return True
        except (requests. ConnectionError, requests. Timeout):
            self.logger.warning("Cant ping sunrise-sunset city")
            return False

    def get_url(self):
        url = f"https://api.sunrise-sunset.org/json?lat=" \
              f"{self.latitude}&lng={self.longitude}&formatted=0"
        self.logger.debug(f"Created current url for sunrise-sunset: {url}")
        return url

    def get_ascii_time(self):
        pass

    def get_human_time(self):
        response = requests.get(self.get_url())
        sun_data = response.json()

        sunrise = sun_data["results"]["sunrise"]
        sunset = sun_data["results"]["sunset"]

        sunrise = datetime.datetime.fromisoformat(sunrise)
        sunset = datetime.datetime.fromisoformat(sunset)

        return f"{sunrise.hour}:{sunrise.minute}", f"{sunset.hour}:{sunset.minute}"
