from os import listdir

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, FallOutTransition, SlideTransition
from kivy.config import Config
from config import Config as AppConfig
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.utils import get_color_from_hex

from screens.status import StatusScreen
from screens.loading import LoadingScreen
from screens.search import SearchScreen
from screens.configuration import ConfigurationScreen

from handlers.city_handlers.open_weather_city_handler import OpenWeatherCityHandler
from handlers.sun_handlers.sunrise_sunset_sun_handler import SunriseSunsetSunHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler


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

    screen_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_screen = None
        self.search_screen = None
        self.loading_screen = None

        self.screen_manager = None
        self.configuration_screen = None

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

        return self.screen_manager

    def _key_handler(self, instance, key, *args):
        if key is 8:
            if not  self.configuration_screen.ids.city_input.focus:
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
            self.screen_manager.current = self.screen_manager.previous()
        elif self.screen_manager.current == "status":
            self.screen_manager.transition = SlideTransition(direction="right")
            self.screen_manager.current = "search"


if __name__ == '__main__':
    WeatherApp().run()
