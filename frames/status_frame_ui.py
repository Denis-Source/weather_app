import tkinter as tk
from config import Config
from PIL import Image, ImageTk


class StatusFrameUI(tk.Frame):
    BLANK_TEMP = -300

    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root
        self.configure(bg=Config.BG_COLOR_PRIMARY)

        self.city_frame = tk.Frame(
            master=self, bg=Config.BG_COLOR_PRIMARY
        )
        self.city_name_label = tk.Label(
            master=self.city_frame, text="City Name", font=(Config.FONT, 32), anchor='w',
            bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
        )
        self.day_name_label = tk.Label(
            master=self.city_frame, text="Monday", font=(Config.FONT, 24), anchor='w',
            bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY

        )
        self.city_time_label = tk.Label(
            master=self.city_frame, text="15:40", font=(Config.FONT, 32), anchor='w',
            bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
        )

        self.weather_frame = tk.Frame(
            master=self, bg=Config.BG_COLOR_PRIMARY)
        self.weather_status = tk.Label(
            master=self.weather_frame, text="Sunny", font=(Config.FONT, 24), anchor='s',
            bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
        )
        self.weather_temperature = tk.Label(
            master=self.weather_frame, text="25°", font=(Config.FONT, 36), anchor='s',
            bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
        )
        self.image_pil = Image.open("images/cloudy.png")
        self.image_pil = self.image_pil.resize((250, 250), Image.ANTIALIAS)
        self.image_pil = ImageTk.PhotoImage(self.image_pil)
        self.weather_image = tk.Label(
            master=self.weather_frame, image=self.image_pil,
            width=250, height=250, bg=Config.BG_COLOR_PRIMARY,
        )

        self.forecast_days_frame = tk.Frame(
            master=self, bg=Config.BG_COLOR_PRIMARY
        )

        self.forecast_frame_list = []
        self.forecast_day_list = []
        self.forecast_temp_list = []

        self.forecast_len = 4

        for i in range(self.forecast_len):
            forecast_frame = tk.Frame(
                master=self.forecast_days_frame, bg=Config.BG_COLOR_PRIMARY
            )
            self.forecast_frame_list.append(forecast_frame)
            forecast_day = tk.Label(
                master=forecast_frame, text="Mon", font=(Config.FONT, 24),
                bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
            )
            self.forecast_day_list.append(forecast_day)
            forecast_temp = tk.Label(
                master=forecast_frame, text="25°", font=(Config.FONT, 20),
                bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY
            )
            self.forecast_temp_list.append(forecast_temp)

    def pack(self):
        super().pack(fill=tk.BOTH, expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.city_frame.grid(row=0, column=0, sticky=tk.NW, padx=(30, 0), pady=(30, 0))

        self.city_name_label.grid(sticky=tk.W)
        self.day_name_label.grid(sticky=tk.W)
        self.city_time_label.grid(sticky=tk.W)

        self.weather_frame.grid(row=0, column=1, sticky=tk.NE, rowspan=3, padx=(0, 30), pady=(30, 0))

        self.weather_status.grid(sticky=tk.E)
        self.weather_temperature.grid(sticky=tk.E)
        self.weather_image.grid(sticky=tk.E, pady=10)

        self.forecast_days_frame.grid(row=2, column=0, sticky=tk.SW, padx=(30, 0), pady=(0, 30))

        for i in range(self.forecast_len):
            self.forecast_frame_list[i].grid(column=i, row=0, ipadx=5)
            self.forecast_day_list[i].grid(sticky=tk.W)
            self.forecast_temp_list[i].grid(sticky=tk.W)

    def set_city_name(self, name):
        self.city_name_label["text"] = name

    def set_day_name(self, name):
        self.day_name_label["text"] = name

    def set_city_time(self, time):
        self.city_time_label["text"] = time

    def set_weather_status(self, status):
        self.weather_status["text"] = status.capitalize()

    def set_weather_temp(self, temp):
        if temp != self.BLANK_TEMP:
            self.weather_temperature["text"] = f"{round(temp)}°"
        else:
            self.weather_temperature["text"] = ""

    def set_weather_image(self, image_path):
        self.image_pil = Image.open(image_path).resize((250, 250), Image.ANTIALIAS)
        self.image_pil = ImageTk.PhotoImage(self.image_pil)

        self.weather_image.configure(image=self.image_pil)
        self.weather_image.image = self.image_pil

    def set_forecast_day(self, n, day, temp):
        self.forecast_day_list[n]["text"] = day
        if temp != self.BLANK_TEMP:
            self.forecast_temp_list[n]["text"] = f"{round(temp)}°"
        else:
            self.forecast_temp_list[n]["text"] = ""

    def _set_bg_of_children(self, elem, new_color):
        for elem in elem.winfo_children():
            elem.configure(bg=new_color)
            if elem:
                self._set_bg_of_children(elem, new_color)

    def set_bg_color(self, new_color):
        self.configure(bg=new_color)
        self._set_bg_of_children(self, new_color)
