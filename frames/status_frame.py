from frames.status_frame_ui import StatusFrameUI

from handlers.errors import WeatherAppException

from datetime import datetime
import time
from config import Config


class StatusFrame(StatusFrameUI):
    def __init__(self, master, weather_handler_class, city_handler_class, sun_handler_class):
        super().__init__(master)
        self.weather_handler_class = weather_handler_class
        self.city_handler_class = city_handler_class
        self.sun_handler_class = sun_handler_class

        self.city = None
        self.current_weather = None
        self.sun_info = None
        self.time_update_task = None

        self.update_time()

    def update_time(self):
        try:
            current_time = datetime.utcfromtimestamp(time.time() + self.current_weather.time_zone)
        except AttributeError:
            current_time = datetime.now()
        self.set_city_time(current_time.strftime("%H:%M"))
        self.set_day_name(current_time.strftime("%A"))

        if self.current_weather:
            self.set_bg_color(self.current_weather.bg_color)

        self.time_update_task = self.master.after(500, self.update_time)

    def update_weather(self, city_name):
        try:
            self.city = self.city_handler_class(city_name).get_city()
            self.sun_info = self.sun_handler_class(self.city).get_ascii_time()
            weather = self.weather_handler_class(self.city).get_weather_current()
            self.current_weather = weather
            self.current_weather.update_state(self.sun_info)
            self.update_current_weather()
            self.update_forecast()
        except WeatherAppException as e:
            self.error(e.message)

    def update_forecast(self):
        forecast = self.weather_handler_class(self.city).get_weather_forecast(4)
        try:
            for i, day_forecast in enumerate(forecast):
                time_stamp = datetime.utcfromtimestamp(day_forecast.time + day_forecast.time_zone)
                day_of_the_week = time_stamp.strftime('%a')
                self.set_forecast_day(i, day_of_the_week, day_forecast.temperature)
        except (NoAPIConnectionException, BadWeatherException, NotCompatibleAPIException) as e:
            self.error(e.message)

    def update_current_weather(self):
        self.set_weather_temp(self.current_weather.temperature)
        self.set_weather_status(self.current_weather.status)
        self.set_weather_image(self.current_weather.image)
        self.set_city_name(self.city.name)

    def error(self, error_name):
        self.set_bg_color(Config.ERROR_COLOR)
        self.set_city_name("Error")
        self.set_weather_status(error_name)
        self.set_weather_image(Config.ERROR_IMAGE)
        self.set_weather_temp(self.BLANK_TEMP)
        self.current_weather = None
        for i in range(self.forecast_len):
            self.set_forecast_day(i, "", self.BLANK_TEMP)

    def set_sun_info(self):
        self.sun_info = self.sun_handler_class(self.city).get_ascii_time()
