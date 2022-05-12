from kivy.animation import Animation
from kivy.uix.screenmanager import Screen


class LoadingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.animation = None

    def animation_stop(self):
        self.animation.stop(self.ids.spinner)
        self.animation = Animation(angle=360, duration=1)
        self.animation.start(self.ids.spinner)

    def animation_start(self):
        self.animation = Animation(angle=360, duration=1)
        self.animation += Animation(angle=360, duration=1)
        self.animation.repeat = True
        self.animation.start(self.ids.spinner)
