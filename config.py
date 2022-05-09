from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Config:
    OPEN_WEATHER_API_KEY = "fdc4b4e12d2b09ba6e3efaf5f08669c3"
    ACCUWEATHER_API_KEY = "6aLfMwtYXqyhy5g1fGFbG1TmoX2XuNAi"

    WIDTH = 640
    HEIGHT = 480

    FONT = "Helvetica"

    BG_COLOR_PRIMARY = "#949cd3"
    FG_COLOR_PRIMARY = "#FFFFFF"

    SUNSET_COLOR = "#df8976"
    DUSK_COLOR = "#949cd3"
    NOON_COLOR = "#90c9ef"
    CLOUD_COLOR = "#96d6f3"
    OVERCAST_COLOR = "#93abd8"
    NIGHT_COLOR = "#3a5e99"
    RAIN_NIGHT_COLOR = "#3e4858"
    RAIN_NOON_COLOR = "#787fa3"
    SNOW_COLOR = "#9d9d9d"

    ERROR_IMAGE = "images/storm.png"
    ERROR_COLOR = "#d85c57"

    LOGGER_FORMAT = "%(asctime)s\t%(levelname)-7s\t%(name)-6s\t%(message)s"
    LOGGING_LEVEL = DEBUG
    LOGGING_FILE = "weather.log"
