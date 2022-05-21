from os import listdir

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, FallOutTransition, SlideTransition, RiseInTransition, NoTransition
from kivy.config import Config
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
    """
    Weather application main class
    Builds the layout and the screen manager
    Adds key listeners

    Screens:
        Search screen with and entry to pass the location name
        Loading screen with the animated spinner
        Status screen to show both the weather and forecast report
        Configuration screen to set the application preferences

    Entirely based on the kivy framework

    Considering the kivy handling of interaction between application and its elements
    The following application object properties created:
        bg_start        background gradient start color
        bg_end          background gradient end color

        time_format     selected time format (12 or 24 hours)
        temp_format     selected temperature format (C or F)

        preferred_city          selected location to load automatically
        preferred_city_to_load  whether to load the location automatically

        weather_handlers    list of all available weather APIS
        city_handlers       list of all available geolocation APIS
        sun_handlers        list of all available sun information APIS

        selected_weather_handler    selected weather API
        selected_city_handler       selected geolocation API
        selected_sun_handler        selected sun information API

        screen_manager
        last_screen
    """
    bg_start = StringProperty(AppConfig.BG_COLOR_PRIMARY[0])
    bg_end = StringProperty(AppConfig.BG_COLOR_PRIMARY[1])

    time_format = ObjectProperty()
    temp_format = ObjectProperty()

    preferred_city = ObjectProperty()
    preferred_city_to_load = ObjectProperty()

    weather_handlers = ObjectProperty()
    city_handlers = ObjectProperty()
    sun_handlers = ObjectProperty()

    selected_weather_handler = ObjectProperty()
    selected_city_handler = ObjectProperty()
    selected_sun_handler = ObjectProperty()

    screen_manager = ObjectProperty()
    last_screen = ObjectProperty()

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.status_screen = None
        self.search_screen = None
        self.loading_screen = None

        self.screen_manager = None
        self.configuration_screen = None

        self.time_format = None
        self.temp_format = None

        self.preferred_city = None
        self.preferred_city_to_load = None

        self.city_handler_class = None
        self.sun_handler_class = None
        self.weather_handler_class = None

        self.weather_handlers = {
            OpenWeatherHandler.API_NAME: OpenWeatherHandler,
            AccuWeatherHandler.API_NAME: AccuWeatherHandler,
            MetaWeatherHandler.API_NAME: MetaWeatherHandler
        }
        self.city_handlers = {
            OpenWeatherCityHandler.API_NAME: OpenWeatherCityHandler,
            AccuWeatherCityHandler.API_NAME: AccuWeatherCityHandler,
            MetaWeatherCityHandler.API_NAME: MetaWeatherCityHandler
        }
        self.sun_handlers = {
            SunriseSunsetSunHandler.API_NAME: SunriseSunsetSunHandler,
            OpenWeatherSunHandler.API_NAME: OpenWeatherSunHandler
        }

        self.selected_weather_handler = None
        self.selected_city_handler = None
        self.selected_sun_handler = None

        self.last_screen = None

    def build(self) -> ScreenManager:
        """
        Builds the application layout
        Loads all of the layouts stored in 'layouts/' folder
        Sets the following configuration:
            No multitouch emulation
            No resizable screen
            No default screen titlebar
        Overrides base kivy application build method
        :return: screen manager with the following screens:
            Search screen with and entry to pass the location name
            Loading screen with the animated spinner
            Status screen to show both the weather and forecast report
            Configuration screen to set the application preferences
        """
        kv_path = "layouts/"
        for kv in listdir(kv_path):
            if kv.endswith(".kv"):
                Builder.load_file(kv_path + kv)

        Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
        Config.set('graphics', 'resizable', False)
        Window.borderless = True

        self.screen_manager = ScreenManager()

        self.status_screen = StatusScreen(name="status")

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

        try:
            self.configuration_screen.load_preferences()
        except (FileNotFoundError, KeyError):
            self.configuration_screen.save_defaults()
            self.configuration_screen.load_preferences()

        self.get_first_screen()

        return self.screen_manager

    def _key_handler(self, instance, key, *args):
        """Binds various keys to events"""
        if not self.screen_manager.current == "loading":
            if key in (8, 27):
                if not self.configuration_screen.ids.auto_city_input.focus:
                    self.set_previous_screen()
                    return True
            elif key == 9:
                if self.screen_manager.current == "search":
                    self.search_screen.ids.city_input.focus = True
            elif key == 13:
                if self.screen_manager.current == "search":
                    self.search_screen.load_city()

    def set_previous_screen(self) -> None:
        """
        Keeps track of the previous screens
        Structures the app (search <- status <- configuration)
        :return: None
        """
        if self.screen_manager.current == "configuration":
            self.screen_manager.transition = FallOutTransition()
            self.screen_manager.current = self.last_screen
        elif self.screen_manager.current == "status":
            self.screen_manager.transition = SlideTransition(direction="right")
            self.screen_manager.current = "search"
            self.last_screen = "search"

    def open_settings(self, *args: list) -> None:
        """
        Opens the configuration screen instead of default kivy screen
        Overrides kivy application method
        :param args:
        :return:
        """
        if self.screen_manager.current != "configuration":
            self.last_screen = self.screen_manager.current
            self.screen_manager.transition = RiseInTransition()
            self.screen_manager.current = "configuration"

    def get_first_screen(self) -> None:
        """
        Works out the screen to be the first one
        Sets the loading screen screen if the preferred location is set
        Sets the status screen otherwise
        :return: None
        """
        if self.preferred_city_to_load:
            self.screen_manager.transition = NoTransition()
            self.screen_manager.current = "loading"
            self.last_screen = self.screen_manager.current
            self.search_screen.load_city(self.preferred_city)
        else:
            self.screen_manager.transition = NoTransition()
            self.screen_manager.current = "search"
            self.last_screen = self.screen_manager.current


if __name__ == '__main__':
    WeatherApp().run()
