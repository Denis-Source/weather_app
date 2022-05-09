class BadCityNameException(Exception):
    def __init__(self, city_name, message="Bad city name"):
        super().__init__(message)
        self.city_name = city_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.city_name}"


class NoAPIConnectionException(Exception):
    def __init__(self, api_name, action, message="No connection"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message
        self.action = action

    def __str__(self):
        return f"{self.message} to {self.api_name} doing {self.action}"


class BadWeatherException(Exception):
    def __init__(self, api_name, message="Bad weather"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message} from {self.api_name}"
