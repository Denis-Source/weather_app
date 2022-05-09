import tkinter as tk
from threading import Thread

from frames.search_frame import SearchFrame
from frames.loading_frame import LoadingFrame
from frames.status_frame import StatusFrame

from config import Config


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.search_frame = SearchFrame(master=self)
        self.loading_frame = LoadingFrame(master=self)
        self.status_frame = StatusFrame(master=self)

        self.geometry("640x480")
        self.configure(bg=Config.BG_COLOR_PRIMARY)
        self.resizable(False, False)

        self.focus_search_frame()

    def focus_search_frame(self, event=None):
        self.search_frame.search_entry.focus()
        self.status_frame.pack_forget()
        self.search_frame.pack()
        self.search_frame.search_button.bind("<Button-1>", self.focus_status_frame)
        self.bind("<Return>", self.focus_status_frame)

    def load_weather(self, city_name):
        self.search_frame.pack_forget()
        self.loading_frame.pack()
        self.status_frame.update_weather(city_name)
        self.loading_frame.pack_forget()
        self.status_frame.pack()

    def focus_status_frame(self, event=None):
        self.status_frame.focus()
        self.unbind("<Return>")
        self.bind("<BackSpace>", self.focus_search_frame)
        city_name = self.search_frame.get_city_name()
        Thread(target=self.load_weather, args=(city_name,)).start()


if __name__ == '__main__':
    WeatherApp().mainloop()