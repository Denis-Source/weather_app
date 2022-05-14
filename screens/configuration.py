from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner, SpinnerOption


class ConfigurationScreen(Screen):
    pass


class APIOption(SpinnerOption):
    pass


class APISpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_cls = APIOption
