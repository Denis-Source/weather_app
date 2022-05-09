import tkinter as tk
from PIL import Image, ImageTk

from config import Config


class SearchFrame(tk.Frame):
    SEARCH_IMAGE_PATH = "images/search.png"
    SEARCH_IMAGE_SIZE = 45

    def __init__(self, **kw):
        super().__init__(**kw)

        self.configure(bg=Config.BG_COLOR_PRIMARY)

        self.search_label = tk.Label(
            master=self, bg=Config.BG_COLOR_PRIMARY, fg=Config.FG_COLOR_PRIMARY, text="Enter City",
            font=(Config.FONT, 32)
        )
        self.search_frame = tk.Frame(master=self, bg=Config.BG_COLOR_PRIMARY)
        self.search_entry = tk.Entry(
            master=self.search_frame, bg=Config.FG_COLOR_PRIMARY, fg=Config.BG_COLOR_PRIMARY, text="Enter City",
            font=(Config.FONT, 28), highlightthickness=0, borderwidth=0, width=15,
        )

        self.search_image = Image.open(self.SEARCH_IMAGE_PATH).resize((self.SEARCH_IMAGE_SIZE, self.SEARCH_IMAGE_SIZE),
                                                                      Image.ANTIALIAS)
        self.search_image = ImageTk.PhotoImage(self.search_image)

        self.search_button = tk.Button(
            master=self.search_frame, bg=Config.BG_COLOR_PRIMARY, fg=Config.BG_COLOR_PRIMARY, width=45, height=45,
            image=self.search_image, highlightthickness=0, borderwidth=0,
        )

    def get_city_name(self):
        return self.search_entry.get()

    def pack(self):
        super().pack()
        self.search_label.pack(pady=(140, 10), padx=(10, 0))
        self.search_frame.pack()
        self.search_entry.grid(ipadx=5, ipady=5, pady=(5, 0))
        self.search_button.grid(row=0, column=1, padx=(10, 0), pady=(5, 0))
