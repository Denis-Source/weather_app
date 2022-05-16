# weather_app
Simple and elegant weather application

## Features
- adaptable color scheme to time of the day and weather conditions
- ability to select weather api
- selectable temprature units and time formats
- simple yet effective location search
- location autosetting
- written in [kivy](https://github.com/Denis-Source/weather_app) and [tkinter](https://github.com/Denis-Source/weather_app/tree/tkinter) GUI frameworks

## >>>
### Search screen
By default the app will ask a location to get weather about.
Location can be entered in any language supported by the APIs.
The search screen can be omitted if default location setting is set.
![image](https://user-images.githubusercontent.com/58669569/168682884-937346e5-e269-4dbb-8cff-fcfff3f02416.png)
Location is determined by the API and that has a comprehensive list of cities and locations all around the world.

### Status screen
When the location was entered applications make several calls to the APIs:
- depending on the selected API gets wether coordinates or [woeid](https://en.wikipedia.org/wiki/WOEID) of the specified location;
- gets information about sun rise or set timings (needed to determine time of the day of the location);
- api call to get current weather information;
- one or several call to get forecast for the next 4 or more days.

If the entered city is correct and api key is correct APIs should return a valid response.

The list of API handlers parse and decode the information to a standart format creating a weather object that contains the following information:
- current tempreture;
- current weather conditions;
- approximate daily forecast for the next 4 days;
- other information witch is stored but not used (wind, humidity, etc).

The main design feature of the application is the ability to change the appearance depending on weather condition and time of the day.
Cloudy weather in New York at 5 evening will have the next theme:
![image](https://user-images.githubusercontent.com/58669569/168685346-d44e7628-0809-4026-8cb5-9174e393fb0a.png)
Clear weather in LA at 2:
![image](https://user-images.githubusercontent.com/58669569/168685412-ca103e04-8647-4dd8-9aae-e1dc7cded1bb.png)
Cloudy weather in Lisbon at dusk:
![image](https://user-images.githubusercontent.com/58669569/168685527-7fca3e9b-e21a-4850-afa9-d967fcc6f622.png)
Night at Kyiv:
![image](https://user-images.githubusercontent.com/58669569/168685582-aef8989b-6a32-4d87-a0e9-87065a11564c.png)
Sunrise at Hong Kong:
![image](https://user-images.githubusercontent.com/58669569/168686351-eedf997f-71a7-4ca6-a30d-333315b081dc.png)




