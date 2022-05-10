class SunInfo:
    def __init__(self, sunrise, sunset):
        self.sunrise = sunrise
        self.sunset = sunset

    def __str__(self):
        return f"Sunrise: {self.sunrise}\n" \
               f"Sunset:  {self.sunset}"
