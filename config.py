from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Config:
    OPEN_WEATHER_API_KEY = "fdc4b4e12d2b09ba6e3efaf5f08669c3"
    ACCUWEATHER_API_KEY = "6aLfMwtYXqyhy5g1fGFbG1TmoX2XuNAi"

    BG_COLOR_PRIMARY = "#bbb3d1", "#7b89cc",
    FG_COLOR_PRIMARY = "#FFFFFF",

    SUNSET_COLOR = "#e3a072", "#dd8078"
    DUSK_COLOR = "#bbb3d1", "#7b89cc"
    NOON_COLOR = "#bbdfd3", "#83c9f3"
    CLOUD_COLOR = "#97dbf8", "#60c3f3"
    OVERCAST_COLOR = "#c5b9bd", "#8990a3"
    NIGHT_COLOR = "#3e64a0", "#21386a"
    RAIN_NIGHT_COLOR = "#85929f", "#434d5d"
    RAIN_NOON_COLOR = "#b2b9d4", "#8990b2"
    SNOW_COLOR = "#c3beca", "#96a0af"

    ERROR_IMAGE = "images/storm.png"
    ERROR_COLOR = "#dd797a", "#d96480"

    LOGGER_FORMAT = "%(asctime)s\t%(levelname)-7s\t%(name)-6s\t%(message)s"
    LOGGING_LEVEL = ERROR
    LOGGING_FILE = "weather.log"
