class City:
    """
    Stores information about a city

    Attributes:
        name
        longitude
        latitude
        woeid       Where On Earth ID of a city
        state       country, state, region etc
    """

    def __init__(self, name: str, longitude: float = None,
                 latitude: float = None, woeid: int = None,
                 state: str = None):
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
               f"Stat: {self.state}"
