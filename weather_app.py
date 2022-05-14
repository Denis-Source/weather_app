import json
from os import listdir

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, FallOutTransition, SlideTransition, RiseInTransition
from kivy.config import Config
from config import Config as AppConfig
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from screens.status import StatusScreen
from screens.loading import LoadingScreen
from screens.search import SearchScreen
from screens.configuration import ConfigurationScreen

from handlers.city_handlers.open_weather_city_handler import OpenWeatherCityHandler
from handlers.city_handlers.accuweather_city_handler import AccuWeatherCityHandler
from handlers.city_handlers.meta_weather_city_handler import MetaWeatherCityHandler

from handlers.sun_handlers.sunrise_sunset_sun_handler import SunriseSunsetSunHandler
from handlers.sun_handlers.open_weather_sun_handler import OpenWeatherSunHandler

from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler
from handlers.weather_handlers.accuweather_handler import AccuWeatherHandler
from handlers.weather_handlers.meta_weather_handler import MetaWeatherHandler

from config import Config as AppConfig


class Loading(Image):
    angle = NumericProperty(0)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class GradientBackground(BoxLayout):
    pass


class WeatherApp(App):
    bg_start = StringProperty(AppConfig.BG_COLOR_PRIMARY[0])
    bg_end = StringProperty(AppConfig.BG_COLOR_PRIMARY[1])

    time_format = ObjectProperty()
    temp_format = ObjectProperty()

    preferred_city = ObjectProperty()
    preferred_city_load = ObjectProperty()

    weather_handlers = ObjectProperty()
    city_handlers = ObjectProperty()
    sun_handlers = ObjectProperty()

    selected_weather_handler = ObjectProperty()
    selected_city_handler = ObjectProperty()
    selected_sun_handler = ObjectProperty()

    screen_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_screen = None
        self.search_screen = None
        self.loading_screen = None

        self.screen_manager = None
        self.configuration_screen = None

        self.time_format = None
        self.temp_format = None

        self.preferred_city = None
        self.preferred_city_load = None

        self.weather_handlers = [
            OpenWeatherHandler,
            AccuWeatherHandler,
            MetaWeatherHandler
        ]
        self.city_handlers = [
            OpenWeatherCityHandler,
            AccuWeatherCityHandler,
            MetaWeatherCityHandler
        ]
        self.sun_handlers = [
            SunriseSunsetSunHandler,
            OpenWeatherSunHandler
        ]

        self.selected_weather_handler = None
        self.selected_city_handler = None
        self.selected_sun_handler = None

    def build(self):
        kv_path = "layouts/"
        for kv in listdir(kv_path):
            if kv.endswith(".kv"):
                Builder.load_file(kv_path + kv)

        Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
        Config.set('graphics', 'resizable', False)
        Window.borderless = True

        self.screen_manager = ScreenManager()

        self.status_screen = StatusScreen(
            OpenWeatherCityHandler,
            SunriseSunsetSunHandler,
            OpenWeatherHandler,

            name="status"
        )

        self.loading_screen = LoadingScreen(name="loading")
        self.search_screen = SearchScreen(name="search")
        self.configuration_screen = ConfigurationScreen(name="configuration")

        self.loading_screen.animation_start()

        self.screen_manager.add_widget(self.search_screen)
        self.screen_manager.add_widget(self.loading_screen)
        self.screen_manager.add_widget(self.status_screen)
        self.screen_manager.add_widget(self.configuration_screen)

        Clock.schedule_interval(self.status_screen.update_time, 0.5)
        Window.bind(on_keyboard=self._key_handler)

        self.screen_manager.current = "search"

        self.load_preferences()

        return self.screen_manager

    def _key_handler(self, instance, key, *args):
        if key in (8, 27):
            if not self.configuration_screen.ids.auto_city_input.focus:
                self.set_previous_screen()
                return True
        elif key is 9:
            if self.screen_manager.current == "search":
                self.search_screen.ids.city_input.focus = True
        elif key is 13:
            if self.screen_manager.current == "search":
                self.search_screen.load_city()

    def set_previous_screen(self):
        if self.screen_manager.current == "configuration":
            self.screen_manager.transition = FallOutTransition()
            self.screen_manager.current = "search"
        elif self.screen_manager.current == "status":
            self.screen_manager.transition = SlideTransition(direction="right")
            self.screen_manager.current = "search"

    def open_settings(self, *args):
        self.screen_manager.transition = RiseInTransition()
        self.screen_manager.current = "configuration"

    def load_preferences(self):
        with open(AppConfig.PREFERENCES_FILE, "r") as f:
            preferences = json.load(f)

        self.time_format = preferences["time_format"]
        self.temp_format = preferences["temp_format"]

        self.preferred_city = preferences["preferred_city"]
        self.preferred_city_load = preferences["preferred_city_load"]

        self.configuration_screen.ids.api_geo_selection.values = [api.API_NAME for api in self.city_handlers]
        self.configuration_screen.ids.api_weather_selection.values = [api.API_NAME for api in self.weather_handlers]
        self.configuration_screen.ids.api_sun_selection.values = [api.API_NAME for api in self.sun_handlers]

        self.selected_city_handler = preferences["city_api"]
        self.selected_weather_handler = preferences["weather_api"]
        self.selected_sun_handler = preferences["sun_api"]

        self.configuration_screen.ids.api_geo_selection.text = self.selected_city_handler
        self.configuration_screen.ids.api_sun_selection.text = self.selected_sun_handler
        self.configuration_screen.ids.api_weather_selection.text = self.selected_weather_handler


if __name__ == '__main__':
    WeatherApp().run()
