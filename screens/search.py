from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, SlideTransition


class SearchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def load_city(self):
        Thread(target=self._load_weather).start()
        self.app.screen_manager.transition = SlideTransition(direction="left")
        self.app.screen_manager.current = "loading"

    def _set_screen_status(self, *args):
        self.app.screen_manager.transition = SlideTransition(direction="left")
        self.app.screen_manager.current = "status"

    def _load_weather(self):
        city_name = self.ids.city_input.text
        self.app.status_screen.set_weather(city_name)
        self.app.status_screen.update_weather()
        Clock.schedule_once(self._set_screen_status)
