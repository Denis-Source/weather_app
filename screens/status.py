import time
from datetime import datetime
from threading import Thread

from kivy.animation import Animation
from kivy.app import App
from kivy.properties import Clock
from kivy.uix.screenmanager import Screen

from handlers.errors import WeatherAppException

from config import Config


class StatusScreen(Screen):
    def __init__(
            self,
            city_handler_class,
            sun_handler_class,
            weather_handler_class,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.city_handler_class = city_handler_class
        self.sun_handler_class = sun_handler_class
        self.weather_handler_class = weather_handler_class

        self.city = None
        self.weather = None
        self.forecast = None
        self.loading_animation = None

    def set_city(self, city_name):
        self.city = self.city_handler_class(city_name).get_city()

    def set_weather(self, city_name):
        try:
            self.set_city(city_name)
            sun_info = self.sun_handler_class(self.city).get_sun_info()
            weather_handler = self.weather_handler_class(self.city)
            self.weather = weather_handler.get_weather_current()
            self.forecast = weather_handler.get_weather_forecast(4)
            self.weather.update_state(sun_info)
        except WeatherAppException as e:
            self.set_error(e.message)

    def refresh_weather(self):
        Thread(target=self._update_weather_animated).start()

    def refresh_animation_stop(self):
        self.loading_animation.stop(self.ids.refresh_button_image)
        self.loading_animation = Animation(angle=360, duration=0.5)
        self.loading_animation.start(self.ids.refresh_button_image)

    def refresh_animation_start(self):
        self.loading_animation = Animation(angle=360, duration=0.5)
        self.loading_animation += Animation(angle=360, duration=0.5)
        self.loading_animation.repeat = True
        self.loading_animation.start(self.ids.refresh_button_image)

    def update_weather(self):
        if self.city:
            self.set_weather(self.city.name)
            if len(self.city.name) > 13:
                self.ids.city_name.text = f"{self.city.name[:11]}..."
            else:
                self.ids.city_name.text = self.city.name

            if self.weather:
                self.ids.weather_status.text = self.weather.status.capitalize()
                self.ids.weather_temp.text = f"{round(self.weather.temperature)}°"
                self.ids.weather_image.source = self.weather.image

                self.ids.forecast_day_1.text = datetime.fromtimestamp(self.forecast[0].time).strftime('%a')
                self.ids.forecast_temp_1.text = f"{round(self.forecast[0].temperature)}°"

                self.ids.forecast_day_2.text = datetime.fromtimestamp(self.forecast[1].time).strftime('%a')
                self.ids.forecast_temp_2.text = f"{round(self.forecast[1].temperature)}°"

                self.ids.forecast_day_3.text = datetime.fromtimestamp(self.forecast[2].time).strftime('%a')
                self.ids.forecast_temp_3.text = f"{round(self.forecast[2].temperature)}°"

                self.ids.forecast_day_4.text = datetime.fromtimestamp(self.forecast[3].time).strftime('%a')
                self.ids.forecast_temp_4.text = f"{round(self.forecast[3].temperature)}°"

                Clock.schedule_once(self.set_background)

    def _update_weather_animated(self):
        self.refresh_animation_start()
        self.update_weather()
        self.refresh_animation_stop()

    def update_time(self, *args):
        try:
            current_time = datetime.utcfromtimestamp(time.time() + self.weather.time_zone)
        except AttributeError:
            current_time = datetime.fromtimestamp(time.time())

        self.ids.city_day.text = current_time.strftime("%A")
        if round(current_time.timestamp()) % 2 == 0:
            self.ids.city_time.text = current_time.strftime("%H:%M")
        else:
            self.ids.city_time.text = current_time.strftime("%H %M")

    def set_background(self, *args):
        App.get_running_app().bg_start = self.weather.color[0]
        App.get_running_app().bg_end = self.weather.color[1]

    def set_error(self, message):
        self.ids.city_name.text = "Error"

        self.ids.weather_status.text = message
        self.ids.weather_temp.text = ""
        self.ids.weather_image.source = Config.ERROR_IMAGE

        self.ids.forecast_day_1.text = ""
        self.ids.forecast_temp_1.text = ""

        self.ids.forecast_day_2.text = ""
        self.ids.forecast_temp_2.text = ""

        self.ids.forecast_day_3.text = ""
        self.ids.forecast_temp_3.text = ""

        self.ids.forecast_day_4.text = ""
        self.ids.forecast_temp_4.text = ""

        App.get_running_app().bg_start = Config.ERROR_COLOR[0]
        App.get_running_app().bg_end = Config.ERROR_COLOR[1]
