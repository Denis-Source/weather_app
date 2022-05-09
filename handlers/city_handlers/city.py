class City:
    def __init__(self, name, longitude, latitude, state=None):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.state = state

    def __str__(self):
        return f"City: {self.name}\n" \
               f"Long: {self.longitude}\n" \
               f"Latd: {self.latitude}\n" \
               f"Stat: {self.state}" \
