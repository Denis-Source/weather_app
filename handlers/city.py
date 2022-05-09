class City:
    def __init__(self, name, longitude=None, latitude=None, info=None, state=None):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.info = info
        self.state = state

    def __str__(self):
        return f"City: {self.name}\n" \
               f"Long: {self.longitude}\n" \
               f"Latd: {self.latitude}\n" \
               f"Info: {self.info}\n" \
               f"Stat: {self.state}" \
