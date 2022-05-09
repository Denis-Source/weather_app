import tkinter as tk
import logging
from threading import Thread

from frames.search_frame import SearchFrame
from frames.loading_frame import LoadingFrame
from frames.status_frame import StatusFrame

from handlers.weather_handlers.accuweather_handler import AccuWeatherHandler
from handlers.city_handlers.accuweather_city_handler import AccuWeatherCityHandler
from handlers.sun_handlers.open_weather_sun_handler import OpenWeatherSunsetHandler


from config import Config


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.search_frame = SearchFrame(master=self)
        self.loading_frame = LoadingFrame(master=self)
        self.status_frame = StatusFrame(
            master=self,
            weather_handler_class=AccuWeatherHandler,
            city_handler_class=AccuWeatherCityHandler,
            sun_handler_class=OpenWeatherSunsetHandler
        )

        self.geometry("640x480")
        self.configure(bg=Config.BG_COLOR_PRIMARY)
        self.resizable(False, False)

        logging.basicConfig(
            format=Config.LOGGER_FORMAT,
            level=Config.LOGGING_LEVEL,
        )

        self.logger = logging.getLogger("app")

        self.logger.info("Starting app")
        self.show_search_frame()

    def show_search_frame(self, event=None):
        self.logger.debug("Starting showing search frame")
        self.search_frame.search_entry.focus()
        self.loading_frame.pack_forget()
        self.status_frame.pack_forget()
        self.search_frame.pack()
        self.search_frame.search_button.bind("<Button-1>", self.show_status_frame)
        self.bind("<Return>", self.show_status_frame)
        self.unbind("<BackSpace>")
        self.logger.info("Showing search frame")

    def load_weather(self, city_name):
        self.logger.debug("Starting loading weather")
        self.loading_frame.start_animation()
        self.search_frame.pack_forget()
        self.logger.info("Showing loading frame")
        self.loading_frame.pack()
        self.status_frame.update_weather(city_name)
        self.loading_frame.pack_forget()
        self.loading_frame.stop_animation()
        self.logger.debug("Starting showing status frame")
        self.status_frame.pack()
        self.bind("<BackSpace>", self.show_search_frame)

    def show_status_frame(self, event=None):
        self.logger.debug("Starting gathering weather status")
        self.status_frame.focus()
        self.unbind("<Return>")
        city_name = self.search_frame.get_city_name()
        Thread(target=self.load_weather, args=(city_name,)).start()


if __name__ == '__main__':
    WeatherApp().mainloop()
