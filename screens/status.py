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
    """
        Status screen to display the current weather conditions and a forecast
        Overrides the kivy screen object
        Attributes:
            city        City object to store the current city
            weather     Weather object to store the current weather conditions
            forecast    Weather list to store the forecast
            loading_animation
            app
        Methods:
            set_city
            set_weather
            refresh_weather
            convert_temp
            update_weather
            update_time
            set_background
            set_error
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.city = None
        self.weather = None
        self.forecast = None
        self.loading_animation = None

    def set_city(self, city_name: str) -> None:
        """
        Gets city information with a handler
        :param city_name: name of the location
        :return: None
        """
        app = App.get_running_app()
        self.city = app.city_handler_class(city_name).get_city()

    def set_weather(self, city_name: str) -> None:
        """
        Gets the current weather report from the handler
        Sets the internal weather attribute
        If the exception occurs resets the city, the weather and the forecast
        and sets the application theme and status screen
        by calling set_error method
        :param city_name: name of the location
        :return: None
        """
        try:
            self.set_city(city_name)
            app = App.get_running_app()
            sun_info = app.sun_handler_class(self.city).get_sun_info()
            weather_handler = app.weather_handler_class(self.city)
            self.weather = weather_handler.get_weather_current()
            self.forecast = weather_handler.get_weather_forecast(4)
            self.weather.update_state(sun_info)
        except WeatherAppException as e:
            self.city = None
            self.weather = None
            self.forecast = None
            self.set_error(e.message)

    def refresh_weather(self) -> None:
        """
        Updates the weather and forecast
        Calls internal method, uses a different thread
        :return: None
        """
        Thread(target=self._update_weather_animated).start()

    def _refresh_animation_stop(self):
        """Stops the rotating spinner animation"""
        self.loading_animation.stop(self.ids.refresh_button_image)
        self.loading_animation = Animation(angle=360, duration=0.5)
        self.loading_animation.start(self.ids.refresh_button_image)

    def _refresh_animation_start(self):
        """Stops the rotating spinner animation, ensures smoothness"""
        self.loading_animation = Animation(angle=360, duration=0.5)
        self.loading_animation += Animation(angle=360, duration=0.5)
        self.loading_animation.repeat = True
        self.loading_animation.start(self.ids.refresh_button_image)

    def convert_temp(self, temp: float, verbose: bool = False) -> str:
        """
        Converts the numeric temperature value from Celsius to Fahrenheit
        Returns a printable string with or without the temperature units name
        :param temp:        numeric temperature value in Celsius
        :param verbose:     whether the sting should contain a unit name
        :return:            prinable string
        """
        app = App.get_running_app()
        if app.temp_format == "C":
            temp_text = f"{round(temp)}°"
        else:
            # C to F conversion rate is t * 9/5 + 32
            temp_text = f"{round(self.weather.temperature * 9/5 + 32)}°"
        if verbose:
            temp_text += app.temp_format
        return temp_text

    def update_weather(self) -> None:
        """
        Updates all the labels with the weather and forecast information
        If the AttributeException is raised does nothing
        :return:
        """
        try:
            self.set_weather(self.city.name)
            # if the city name is too long, truncates it
            if len(self.city.name) > 13:
                self.ids.city_name.text = f"{self.city.name[:10]}..."
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

    def _update_weather_animated(self) -> None:
        """Updates the weather with the spinner animation"""
        self._refresh_animation_start()
        self.update_weather()
        self._refresh_animation_stop()

    def update_time(self, *args) -> None:
        """
        Updates the time
        Despite of weather report having a time stamp
        it based on the local operating system time
        To calculate the proper location time it uses a time zone of the location
        If no city object are stored, no timezones are used
        :param args: list
        :return:
        """
        try:
            current_time = datetime.utcfromtimestamp(time.time() + self.weather.time_zone)
        except AttributeError:
            current_time = datetime.fromtimestamp(time.time())

        self.ids.city_day.text = current_time.strftime("%A")
        app = App.get_running_app()
        if app.time_format == 24:
            time_format = "%H:%M"
        else:
            time_format = "%H:%M %p"

        time_text = current_time.strftime(time_format)

        if round(current_time.timestamp()) % 2 == 0:
            self.ids.city_time.text = time_text
        else:
            self.ids.city_time.text = time_text.replace(":", " ")

    def set_background(self, *args) -> None:
        """Sets the application theme"""
        app = App.get_running_app()
        app.bg_start = self.weather.color[0]
        app.bg_end = self.weather.color[1]

    def set_error(self, message: str) -> None:
        """
        Prints the error message on the screen
        Sets the application theme
        Sets all the labels with falsy values to make them blank
        :param message: Error message
        :return: None
        """
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

        app = App.get_running_app()
        app.bg_start = Config.ERROR_COLOR[0]
        app.bg_end = Config.ERROR_COLOR[1]
