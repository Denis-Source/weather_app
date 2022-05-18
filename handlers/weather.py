from config import Config
from handlers.sun_info import SunInfo


class Weather:
    """
    Weather status to track various information

    Attributes:
        location_name   name of the tracked location
        status          weather  condition name
        color           colors associated with the weather (tuple)
        image           image associated with the weather (image folder)
        temperature     temperature in Celsius
        pressure        pressure in inches of mercury
        humidity        humidity percentage (from 0 to 100)
        wind_speed      wind speed in meters per second
        wind_direction  wind direction in degrees (from 0 to 360)
        time: epoch     time in seconds
        time_zone       time zone in seconds

    Time constants:
        SUNSET_PERIOD   How much time is needed to be close to the
                        sunrise or sunset to set sunrise theme
        DUSK_PERIOD     How much time is needed to be close to the
                        sunrise or sunset to set dusk theme

    Weather conditions:
        CLEAR, CLOUDY, OVERCAST, SUNNY_RAIN, RAIN,
        THUNDERSTORM, SNOW, MIST, SANDSTORM, ERUPTION, STORM,
        NIGHT_CLEAR, NIGHT_CLOUDY, SUNRISE

    IMAGE_TABLE         Maps weather status to the corresponding images
    """

    SUNSET_PERIOD = 30 * 60
    DUSK_PERIOD = 120 * 60

    CLEAR = "clear sky"
    CLOUDY = "cloudy"
    OVERCAST = "overcast"
    SUNNY_RAIN = "sunny rain"
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    SNOW = "snow"
    MIST = "mist"
    SANDSTORM = "sand storm"
    ERUPTION = "eruption"
    STORM = "tornado"

    NIGHT_CLEAR = "night_clear"
    NIGHT_CLOUDY = "night_cloudy"
    SUNRISE = "sunrise"

    IMAGE_TABLE = {
        CLEAR: "images/sunny.png",
        CLOUDY: "images/cloudy.png",
        OVERCAST: "images/overcast.png",
        SUNNY_RAIN: "images/sunny_rain.png",
        RAIN: "images/rain.png",
        THUNDERSTORM: "images/thunderstorm.png",
        SNOW: "images/snow.png",
        MIST: "images/mist.png",
        SANDSTORM: "images/sand.png",
        ERUPTION: "images/eruption.png",
        STORM: "images/storm.png",
        NIGHT_CLEAR: "images/moon.png",
        NIGHT_CLOUDY: "images/night_cloudy.png",
        SUNRISE: "images/sunrise.png"
    }

    def __init__(
            self, location_name: str = None, status: str = None, temperature: float = None,
            pressure: float = None, humidity: float = None, wind_speed: float = None,
            wind_direction: float = None, time: float = None, time_zone: float = None
    ):
        """Weather instance constructor"""

        self.city_name = location_name

        self.status = status
        self.image = self.IMAGE_TABLE[status]
        self.color = None

        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

        self.time = time
        self.time_zone = time_zone

    def update_state(self, sun_info: SunInfo):
        """
        Method to update internal state
        Sets weather color and images depending on time and conditions
        :param sun_info: SunInfo object to store sunset and sunrise timings
        :return: None
        """

        # Sets snowy theme
        if self.status == self.SNOW or self.status == self.MIST:
            self.color = Config.SNOW_COLOR
            return

        # Sets sunset/sunrise theme
        if abs(sun_info.sunrise - self.time) < self.SUNSET_PERIOD \
                or abs(sun_info.sunset - self.time) < self.SUNSET_PERIOD:
            self.image = self.IMAGE_TABLE[self.SUNRISE]
            self.color = Config.SUNSET_COLOR
            return

        # Sets dusk theme
        if abs(sun_info.sunset - self.time) < self.DUSK_PERIOD:
            self.color = Config.DUSK_COLOR
            return

        # determine whether there is a day or night
        if sun_info.sunrise < self.time < sun_info.sunset:
            is_day = True
        else:
            is_day = False

        # eruption theme
        if self.status == self.ERUPTION:
            self.color = Config.SUNSET_COLOR
            return

        # thunder storm theme
        if self.status == self.RAIN or self.status == self.THUNDERSTORM:
            if is_day:
                self.color = Config.RAIN_NOON_COLOR
            else:
                self.color = Config.RAIN_NIGHT_COLOR
            return

        # clear theme
        if self.status == self.CLEAR:
            if is_day:
                self.color = Config.NOON_COLOR
                return
            else:
                self.image = self.IMAGE_TABLE[self.NIGHT_CLEAR]
                self.color = Config.NIGHT_COLOR
                return

        # cloudy theme
        if self.status == self.CLOUDY:
            if is_day:
                self.color = Config.CLOUD_COLOR
                return
            else:
                self.color = Config.NIGHT_COLOR
                self.image = self.IMAGE_TABLE[self.NIGHT_CLOUDY]
                return

        # overcast theme
        if self.status == self.OVERCAST:
            if is_day:
                self.color = Config.OVERCAST_COLOR
                return
            else:
                self.color = Config.NIGHT_COLOR
                return

        # default is dusk theme
        self.color = Config.DUSK_COLOR

    def __str__(self):
        """
        Printable string of the object
        :return: str
        """
        return f"City: {self.city_name}\n" \
               f"Stat: {self.status}\n" \
               f"Imag: {self.image}\n" \
               f"Colr: {self.color}\n" \
               f"Temp: {self.temperature}\n" \
               f"Pres: {self.pressure}\n" \
               f"Humd: {self.humidity}\n" \
               f"WndS: {self.wind_speed}\n" \
               f"WndD: {self.wind_direction}\n" \
               f"Time: {self.time}\n" \
               f"Tzne: {self.time_zone}\n"
