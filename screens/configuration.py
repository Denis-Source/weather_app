import json

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner, SpinnerOption

from config import Config


class ConfigurationScreen(Screen):
    """
    Configuration Screen is used to setup preferences of the application
    Uses preferences.json file
    Has the following settings:
        Time format (24 or 12 hours);
        Temperature units (Celsius or Fahrenheit
        Weather handler class
        City handler class
        Sun handler class
        Auto location setting
        Preferred city (when auto location setting is on)
    Overrides the kivy screen object

    Methods:
        load_preferences
        save_preferences
        save_defaults
    """

    def load_preferences(self) -> None:
        """
        Loads settings from the preferences.json file
        Sets root application object accordingly
        Sets buttons and entries
        Loads all the settings listed above in one go
        :return: None
        """
        app = App.get_running_app()

        with open(Config.PREFERENCES_FILE, "r") as f:
            preferences = json.load(f)

        app.time_format = preferences["time_format"]
        if app.time_format == 24:
            self.ids.toggle_time_24.state = "down"
        else:
            self.ids.toggle_time_12.state = "down"

        app.temp_format = preferences["temp_format"]
        if app.temp_format == "C":
            self.ids.toggle_temp_cels.state = "down"
        else:
            self.ids.toggle_temp_fahr.state = "down"

        self.ids.api_geo_selection.values = [api for api in app.city_handlers]
        self.ids.api_weather_selection.values = [api for api in app.weather_handlers]
        self.ids.api_sun_selection.values = [api for api in app.sun_handlers]

        app.selected_city_handler = preferences["city_api"]
        app.selected_weather_handler = preferences["weather_api"]
        app.selected_sun_handler = preferences["sun_api"]

        self.ids.api_geo_selection.text = app.selected_city_handler
        self.ids.api_sun_selection.text = app.selected_sun_handler
        self.ids.api_weather_selection.text = app.selected_weather_handler

        app.preferred_city_to_load = preferences["preferred_city_to_load"]
        app.preferred_city = preferences["preferred_city"]

        if app.preferred_city_to_load:
            self.ids.auto_city_on_toggle.state = "down"
            self.ids.auto_city_off_toggle.state = "normal"
            self.ids.auto_city_input.text = app.preferred_city
        else:
            self.ids.auto_city_off_toggle.state = "down"
            self.ids.auto_city_on_toggle.state = "normal"
            self.ids.auto_city_input.text = ""
            app.preferred_city = ""

        app.city_handler_class = app.city_handlers[app.selected_city_handler]
        app.sun_handler_class = app.sun_handlers[app.selected_sun_handler]
        app.weather_handler_class = app.weather_handlers[app.selected_weather_handler]

    def save_preferences(self) -> None:
        """
        Saves settings from the configuration screen to the preferences.json file
        gets the information from the buttons and entries
        Saves all the settings listed above in one go
        After saving loads the settings repeatedly to ensure synchronicity
        :return: None
        """
        app = App.get_running_app()

        if self.ids.toggle_time_24.state == "down":
            app.time_format = 24
        else:
            app.time_format = 12

        if self.ids.toggle_temp_cels.state == "down":
            app.temp_format = "C"
        else:
            app.temp_format = "F"

        app.selected_city_handler = self.ids.api_geo_selection.text
        app.selected_sun_handler = self.ids.api_sun_selection.text
        app.selected_weather_handler = self.ids.api_weather_selection.text

        if self.ids.auto_city_on_toggle.state == "down" \
                and self.ids.auto_city_input.text:
            app.preferred_city_to_load = True
            app.preferred_city = self.ids.auto_city_input.text
        else:
            app.preferred_city_to_load = False
            app.preferred_city = ""

        preferences = {
            "time_format": app.time_format,
            "temp_format": app.temp_format,
            "city_api": app.selected_city_handler,
            "weather_api": app.selected_weather_handler,
            "sun_api": app.selected_sun_handler,
            "preferred_city_to_load": app.preferred_city_to_load,
            "preferred_city": app.preferred_city
        }

        with open(Config.PREFERENCES_FILE, "w") as f:
            json.dump(preferences, f, indent=2)

        self.load_preferences()

    def save_defaults(self) -> None:
        """
        Saves the default configuration in the preferences.json file
        :return:
        """
        defaults = {
            "time_format": 24,
            "temp_format": "C",
            "city_api": list(self.city_handlers)[0],
            "weather_api": list(self.weather_handlers)[0],
            "sun_api": list(self.sun_handlers)[0],
            "preferred_city_to_load": False,
            "preferred_city": ""
        }
        with open(Config.PREFERENCES_FILE, "w") as f:
            json.dump(defaults, f, indent=2)


class APIOption(SpinnerOption):
    """API Spinner option class"""
    pass


class APISpinner(Spinner):
    """API Spinner class with the defined option class"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_cls = APIOption
