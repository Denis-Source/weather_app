class City:
    def __init__(self, name, longitude=None, latitude=None, woeid=None, state=None):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.woeid = woeid
        self.state = state

    def __str__(self):
        return f"City: {self.name}\n" \
               f"Long: {self.longitude}\n" \
               f"Latd: {self.latitude}\n" \
               f"Info: {self.woeid}\n" \
               f"Stat: {self.state}" \
