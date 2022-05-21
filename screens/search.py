from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, SlideTransition


class SearchScreen(Screen):
    """
    Search screen is based on the location entry and search button
    After the location is entered loads weather information by calling
    the corresponding method of the status screen
    Overrides the kivy screen object

    Methods:
        load_city
    """

    def load_city(self, city_name: str = None) -> None:
        """
        Gets the location name and makes an API call
        Uses the similar internal method to make a call on a different thread
        :param city_name:
        :return: None
        """
        app = App.get_running_app()
        Thread(target=self._load_weather, args=(city_name,)).start()
        app.screen_manager.transition = SlideTransition(direction="left")
        app.screen_manager.current = "loading"

    def _set_screen_status(self, *args):
        app = App.get_running_app()
        app.screen_manager.transition = SlideTransition(direction="left")
        app.screen_manager.current = "status"

    def _load_weather(self, city_name):
        app = App.get_running_app()

        if not city_name:
            city_name = self.ids.city_input.text
        app.status_screen.set_weather(city_name)
        app.status_screen.update_weather()
        # considering that the kivy framework does not allow
        # to change graphics on the different thread
        # a clock object is used
        Clock.schedule_once(self._set_screen_status)
