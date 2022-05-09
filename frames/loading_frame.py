import tkinter as tk
from PIL import ImageTk, Image

from config import Config


class LoadingFrame(tk.Frame):
    SPINNER_PATH = "images/spinner.png"
    IMAGE_SIZE = 100
    REFRESH_INTERVAL = 4

    def __init__(self, master, **kw):
        super().__init__(height=Config.HEIGHT, **kw)
        self.master = master
        self.spinner_image = None
        self.configure(bg=Config.BG_COLOR_PRIMARY)
        self.canvas = tk.Canvas(master=self, bg=Config.BG_COLOR_PRIMARY, highlightthickness=0,
                                width=self.IMAGE_SIZE, height=self.IMAGE_SIZE)
        self.configure(height=Config.WIDTH)
        self.to_animate = False
        self.update = None

    def load_image(self):
        self.spinner_image = Image.open(self.SPINNER_PATH).resize((self.IMAGE_SIZE, self.IMAGE_SIZE), Image.ANTIALIAS)

    def start_animation(self):
        self.to_animate = True
        self.update = self.draw().__next__
        self.master.after(self.REFRESH_INTERVAL, self.update)

    def stop_animation(self):
        self.to_animate = False

    def draw(self):
        self.load_image()
        angle = 0
        while True:
            rotated_image = ImageTk.PhotoImage(self.spinner_image.rotate(angle))
            canvas_image = self.canvas.create_image(
                self.IMAGE_SIZE, self.IMAGE_SIZE, image=rotated_image, anchor=tk.SE)
            if self.to_animate:
                self.master.after(self.REFRESH_INTERVAL, self.update)
            yield
            self.canvas.delete(canvas_image)
            angle += 10
            angle %= 360

    def pack(self):
        super().pack()
        self.pack_propagate(0)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid(pady=(Config.HEIGHT / 2 - self.IMAGE_SIZE / 2, 0), sticky=tk.S)
