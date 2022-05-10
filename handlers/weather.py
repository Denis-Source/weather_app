from config import Config
from handlers.sun_info import SunInfo


class Weather:
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
        STORM: "images/storm.png"
    }

    def __init__(
            self, city_name=None, status=None, temperature=None,
            pressure=None, humidity=None, wind_speed=None,
            wind_direction=None, time=None, time_zone=None
    ):
        self.city_name = city_name

        self.status = status
        self.image = self.IMAGE_TABLE[status]
        self.bg_color = None

        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

        self.time = time
        self.time_zone = time_zone

    def update_state(self, sun_info: SunInfo):
        if self.status == self.SNOW or self.status == self.MIST:
            self.bg_color = Config.SNOW_COLOR
            return

        if abs(sun_info.sunrise - self.time) < self.SUNSET_PERIOD \
                or abs(sun_info.sunset - self.time) < self.SUNSET_PERIOD:
            self.image = "images/sunrise.png"
            self.bg_color = Config.SUNSET_COLOR
            return

        if abs(sun_info.sunset - self.time) < self.DUSK_PERIOD:
            self.bg_color = Config.DUSK_COLOR
            return

        if sun_info.sunrise < self.time < sun_info.sunset:
            is_day = True
        else:
            is_day = False

        if self.status == self.ERUPTION:
            self.bg_color = Config.SUNSET_COLOR
            return

        if self.status == self.RAIN or self.status == self.THUNDERSTORM:
            if is_day:
                self.bg_color = Config.RAIN_NOON_COLOR
            else:
                self.bg_color = Config.RAIN_NIGHT_COLOR
            return

        if self.status == self.CLEAR:
            if is_day:
                self.bg_color = Config.NOON_COLOR
                return
            else:
                self.image = "images/moon.png"
                self.bg_color = Config.NIGHT_COLOR
                return

        if self.status == self.CLOUDY:
            if is_day:
                self.bg_color = Config.CLOUD_COLOR
                return
            else:
                self.bg_color = Config.NIGHT_COLOR
                self.image = "images/night_cloudy.png"
                return

        if self.status == self.OVERCAST:
            if is_day:
                self.bg_color = Config.OVERCAST_COLOR
                return
            else:
                self.bg_color = Config.NIGHT_COLOR
                return

        self.bg_color = Config.DUSK_COLOR

    def __str__(self):
        return f"City: {self.city_name}\n" \
               f"Stat: {self.status}\n" \
               f"Imag: {self.image}\n" \
               f"Colr: {self.bg_color}\n" \
               f"Temp: {self.temperature}\n" \
               f"Pres: {self.pressure}\n" \
               f"Humd: {self.humidity}\n" \
               f"WndS: {self.wind_speed}\n" \
               f"WndD: {self.wind_direction}\n" \
               f"Time: {self.time}\n" \
               f"Tzne: {self.time_zone}\n"
