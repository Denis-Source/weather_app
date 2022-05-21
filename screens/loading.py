from kivy.animation import Animation
from kivy.uix.screenmanager import Screen


class LoadingScreen(Screen):
    """
    Loading Screen is used to fill lengthy operations
    Overrides the kivy screen object

    Attributes:
        animation
    Methods:
        animation_stop
        animation_start
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.animation = None

    def animation_stop(self) -> None:
        """
        Stops the animation
        To ensure smoothness continues the rotation to the 360 degree angle
        by starting a new non-repeatable animation
        :return:
        """
        self.animation.stop(self.ids.spinner)
        self.animation = Animation(angle=360, duration=1)
        self.animation.start(self.ids.spinner)

    def animation_start(self) -> None:
        """
        Sets the spinning animation of the image in the layout
        Rotates the image once per second
        Makes rotation repeatable

        :return:
        """
        self.animation = Animation(angle=360, duration=1)
        self.animation += Animation(angle=360, duration=1)
        self.animation.repeat = True
        self.animation.start(self.ids.spinner)
