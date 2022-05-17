# weather_app
Simple yet elegant weather application

## Features
- adaptable color scheme to time of the day and weather conditions;
- ability to select weather api;
- selectable temperature units and time formats;
- simple yet effective location search;
- location autosetting;
- written in [kivy](https://github.com/Denis-Source/weather_app) and [tkinter](https://github.com/Denis-Source/weather_app/tree/tkinter) GUI frameworks.
***

## Installation
Weather app uses kivy as a frontend framework and can be installed on both mobile and desktop platforms.
Installation process:
```shell
git clone https://github.com/Denis-Source/weather_app
cd weather_app
```
It is recommended to use venv
Windows:
```shell
python -m venv venv
venv\Scripts\Activate.ps1
pip install - requirements.txt
```
Linux/MacOS:
```shell
python3 -m venv venv
source venv/bin/activate
pip install - requirements.txt
```

In order to use the app you should have API keys. For testing purposes, you can use MetaWeather and Sunset and Sunrise APIs.
To run the app. simply start the main file:
```shell
python weather_app.py
```
***

## Showcase
### Search screen
By default, the app will ask a location to get weather about.
The location can be entered in any language supported by the APIs.
The search screen can be omitted if the default location setting is set.
![image](https://user-images.githubusercontent.com/58669569/168682884-937346e5-e269-4dbb-8cff-fcfff3f02416.png)
Location is determined by the API and it has a comprehensive list of cities and locations all around the world.

### Status screen
When the location was entered, the application makes several calls to the APIs:
- depending on whether the selected API gets the coordinates or the [woeid](https://en.wikipedia.org/wiki/WOEID) of the specified location;
- gets information about sun rise or set timings (needed to determine time of the day of the location);
- api call to get current weather information;
- one or several calls to get a forecast for the next 4 or more days.

If the entered city is correct and the API key is correct, the API should return a valid response.

The list of API handlers that parse and decode the information to a standard format, creating a weather object that contains the following information:
- current temperature;
- current weather conditions;
- approximate daily forecast for the next 4 days;
- other information which is stored but not used (wind, humidity, etc).

The main design feature of the application is the ability to change it's appearance depending on weather conditions and time of the day.

#### Cloudy weather in New York at 5 in the evening will have the next theme:
![image](https://user-images.githubusercontent.com/58669569/168685346-d44e7628-0809-4026-8cb5-9174e393fb0a.png)
#### Clear weather in LA at 2:
![image](https://user-images.githubusercontent.com/58669569/168685412-ca103e04-8647-4dd8-9aae-e1dc7cded1bb.png)
#### Cloudy weather in Lisbon at dusk:
![image](https://user-images.githubusercontent.com/58669569/168685527-7fca3e9b-e21a-4850-afa9-d967fcc6f622.png)
#### Night in Kyiv:
![image](https://user-images.githubusercontent.com/58669569/168685582-aef8989b-6a32-4d87-a0e9-87065a11564c.png)
#### Sunrise in Hong Kong:
![image](https://user-images.githubusercontent.com/58669569/168686351-eedf997f-71a7-4ca6-a30d-333315b081dc.png)
***

## Customization
The application allows you to change time format, temperature units as well as, called APIs. All this work can be done via the configuration screen (menu button or `f1` key).
The screen theme is also dynamically changed.

#### Example of the configuration screen:
![image](https://user-images.githubusercontent.com/58669569/168776566-33ff656d-85dc-4981-84d3-360d77940c46.png)

There is an option to define the default location.
#### The default can be set in the form:
![image](https://user-images.githubusercontent.com/58669569/168777220-e44c783d-2e57-4cf0-9833-f3fc1878b992.png)
***

## APIs
The application has 3 or 4 different types of APIs:
- geolocation;
- sunrise and sunset information about the location;
- current weather information;
- average forecast for the following 4 or more days.

The architecture of the app allows dynamic selection of APIs on the fly.
#### Selection of APIs for weather reports:
![image](https://user-images.githubusercontent.com/58669569/168777910-3319f211-c63b-46f5-8a85-99479702802b.png)

As the latest version is considered, there are the following available APIs:
- [OpenWeather](https://openweathermap.org/api): geolocation, weather and sun information;
- [AccuWeather](https://developer.accuweather.com/): geolocation and weather;
- [MetaWeather](https://www.metaweather.com/api/): geolocation and weather;
- [Sunset and Sunrise](https://sunrise-sunset.org/api): sun information.

Some of them require an API key and allow a limited daily requests amount; others are free.

> Note: Some APIs use [woeid](https://en.wikipedia.org/wiki/WOEID) and other longitude and latitude, so as a consequence they, are not compatible.

