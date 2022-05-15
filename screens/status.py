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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.city = None
        self.weather = None
        self.forecast = None
        self.loading_animation = None
        self.app = App.get_running_app()

    def set_city(self, city_name):
        self.city = self.app.city_handler_class(city_name).get_city()

    def set_weather(self, city_name):
        try:
            self.set_city(city_name)
            sun_info = self.app.sun_handler_class(self.city).get_sun_info()
            weather_handler = self.app.weather_handler_class(self.city)
            self.weather = weather_handler.get_weather_current()
            self.forecast = weather_handler.get_weather_forecast(4)
            self.weather.update_state(sun_info)
        except WeatherAppException as e:
            self.city = None
            self.weather = None
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

    def convert_temp(self, temp, verbose=False):
        if self.app.temp_format == "C":
            temp_text = f"{round(temp)}°"
        else:
            temp_text = f"{round(self.weather.temperature * 9 / 5 + 32)}°"
        if verbose:
            temp_text += self.app.temp_format
        return temp_text

    def update_weather(self):
        try:
            self.set_weather(self.city.name)
            if len(self.city.name) > 13:
                self.ids.city_name.text = f"{self.city.name[:11]}..."
            else:
                self.ids.city_name.text = self.city.name

            if self.weather:
                self.ids.weather_status.text = self.weather.status.capitalize()
                self.ids.weather_temp.text = self.convert_temp(self.weather.temperature, verbose=True)
                self.ids.weather_image.source = self.weather.image

                self.ids.forecast_day_1.text = datetime.fromtimestamp(self.forecast[0].time).strftime('%a')
                self.ids.forecast_temp_1.text = self.convert_temp(self.forecast[0].temperature)

                self.ids.forecast_day_2.text = datetime.fromtimestamp(self.forecast[1].time).strftime('%a')
                self.ids.forecast_temp_2.text = self.convert_temp(self.forecast[1].temperature)

                self.ids.forecast_day_3.text = datetime.fromtimestamp(self.forecast[2].time).strftime('%a')
                self.ids.forecast_temp_3.text = self.convert_temp(self.forecast[2].temperature)

                self.ids.forecast_day_4.text = datetime.fromtimestamp(self.forecast[3].time).strftime('%a')
                self.ids.forecast_temp_4.text = self.convert_temp(self.forecast[3].temperature)

                Clock.schedule_once(self.set_background)
        except AttributeError:
            pass

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
        if self.app.time_format == 24:
            time_format = "%H:%M"
        else:
            time_format = "%H:%M %p"

        time_text = current_time.strftime(time_format)

        if round(current_time.timestamp()) % 2 == 0:
            self.ids.city_time.text = time_text
        else:
            self.ids.city_time.text = time_text.replace(":", " ")

    def set_background(self, *args):
        self.app.bg_start = self.weather.color[0]
        self.app.bg_end = self.weather.color[1]

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

        self.app.bg_start = Config.ERROR_COLOR[0]
        self.app.bg_end = Config.ERROR_COLOR[1]
