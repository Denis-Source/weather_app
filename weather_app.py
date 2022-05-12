from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from config import Config as AppConfig
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty

from screens.status import StatusScreen
from screens.loading import LoadingScreen
from screens.search import SearchScreen

from handlers.city_handlers.open_weather_city_handler import OpenWeatherCityHandler
from handlers.sun_handlers.sunrise_sunset_sun_handler import SunriseSunsetSunHandler
from handlers.weather_handlers.open_weather_handler import OpenWeatherHandler


class WeatherApp(App):
    bg_start = StringProperty(AppConfig.BG_COLOR_PRIMARY[0])
    bg_end = StringProperty(AppConfig.BG_COLOR_PRIMARY[1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_screen = None
        self.search_screen = None
        self.loading_screen = None

        self.screen_manager = None

    def build(self):
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

        self.loading_screen.animation_start()

        self.screen_manager.add_widget(self.search_screen)
        self.screen_manager.add_widget(self.status_screen)
        self.screen_manager.add_widget(self.loading_screen)

        Clock.schedule_interval(self.status_screen.update_time, 0.5)

        return self.screen_manager


if __name__ == '__main__':
    WeatherApp().run()
