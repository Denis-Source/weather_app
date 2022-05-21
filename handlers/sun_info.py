class SunInfo:
    """
    Stores sunrise and sunset timings

    Arguments:
        sunrise     epoch time of the sunrise
        sunset      epoch time of the sunset
    """
    def __init__(self, sunrise, sunset):
        self.sunrise = sunrise
        self.sunset = sunset

    def __str__(self):
        return f"Sunrise: {self.sunrise}\n" \
               f"Sunset:  {self.sunset}"
