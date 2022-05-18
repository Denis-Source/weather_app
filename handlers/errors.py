class WeatherAppException(Exception):
    def __init__(self, message="Unspecified"):
        super().__init__(message)
        self.message = message


class BadCityNameException(WeatherAppException):
    def __init__(self, city_name, message="Bad city name"):
        super().__init__(message)
        self.city_name = city_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.city_name}"


class NoAPIConnectionException(WeatherAppException):
    def __init__(self, api_name, action, message="No connection"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message
        self.action = action

    def __str__(self):
        return f"{self.message} to {self.api_name} doing {self.action}"


class BadWeatherException(WeatherAppException):
    def __init__(self, api_name, message="Bad weather"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message} from {self.api_name}"


class NotCompatibleAPIException(WeatherAppException):
    def __init__(self, api_name, message="Not compatible apis"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.api_name}"


class ServiceUnavailableException(WeatherAppException):
    def __init__(self, api_name, message="API unavailable"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.api_name}"

