class WeatherAppException(Exception):
    """
    General Exception with a default message

    Attributes:
        message
    """

    def __init__(self, message: str = "Unspecified"):
        super().__init__(message)
        self.message = message


class BadCityNameException(WeatherAppException):
    """
    Bad name or unknown location Exception
    Inherits WeatherAppException

    Attributes:
        city_name
        message
    """

    def __init__(self, city_name: str, message: str = "Bad city name"):
        super().__init__(message)
        self.city_name = city_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.city_name}"


class NoAPIConnectionException(WeatherAppException):
    """
    Raised when the API is not reachable
    Inherits WeatherAppException

    Attributes:
        api_name
        message
        action      action caused the exception
    """

    def __init__(self, api_name: str, action: str, message: str = "No connection"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message
        self.action = action

    def __str__(self):
        return f"{self.message} to {self.api_name} doing {self.action}"


class BadWeatherException(WeatherAppException):
    """
    Usually raised when the weather answer is not parsable
    Inherits WeatherAppException

    Attributes:
        api_name
        message
    """

    def __init__(self, api_name: str, message: str = "Bad weather"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message} from {self.api_name}"


class NotCompatibleAPIException(WeatherAppException):
    """
    Raised when API that used for a geolocation is not compatible
    with the weather API
    For example a geolocation API sets woeid but a weather one
    demands latitude and longitude
    Inherits WeatherAppException

    Attributes:
        api_name
        message
    """

    def __init__(self, api_name: str, message: str = "Not compatible apis"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.api_name}"


class ServiceUnavailableException(WeatherAppException):
    """
    Raised when API that responded with an error response
    Unlike NoAPIConnectionException this exception is raised when an API is reachable
    Inherits WeatherAppException

    Attributes:
        api_name
        message
    """

    def __init__(self, api_name: str, message: str = "API unavailable"):
        super().__init__(message)
        self.api_name = api_name
        self.message = message

    def __str__(self):
        return f"{self.message}: {self.api_name}"
