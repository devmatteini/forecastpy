# ForecastPy

A python package to interact with the OpenWeatherAPI in a simple and fast way.

[Live demo](https://devmc.pythonanywhere.com) here.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Documentation](#documentation)
  - [Dependencies](#dependencies)
  - [Unit](#unit)
  - [Days](#days)
  - [Weather](#weather)
  - [Errors](#errors)
- [Built With](#built-With)
- [Version](#version)
- [Author](#author)
- [Licence](#license)

## Getting Started

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ForecastPy.

```
pip install forecastpy
```

### Usage

```
from forecastpy import Weather, Unit, Days

# Init Weather object with your open weather api key
weather = Weather('YOUR_API_KEY')

# Get current weather from a city name
w = weather.get_current_weather('CITY_NAME', Unit.METRIC)

# Get weather for more than one day
w2 = weather.get_days_weather('CITY_NAME', Unit.METRIC, Days.TWO)
```

## Documentation

### Dependencies

Python packages:

- json
- requests
- datetime

### Unit

Unit is a class which makes thing easier when you have to choose the unit type you want from the weather forecast.
The available units are:

- Kelvin (Default option)
- Metric
- Fahrenheit

##### Usage

```
Unit.METRIC # return 'metric'
Unit.FAHRENHEIT # return 'imperail'
```

### Days

Days is a class which makes thing easier when you have to choose the number of days you want.
The lowest number is 2 and the maximum is 5 (which is the higher number of day set on the free version of the OpenWeatherAPI)

The available days are:

- Two
- Three
- Four
- Five (Default option)

##### Usage

```
Days.TWO # return 2
Days.THREE # return 3
...
```

### Weather

Weather is the class you'll need to use to interact with the OpenWeatherAPI.
It requires the OpenWeatherAPI key as its only parameter when you have to initialize it.
Learn more about the [OpenWeatherAPI](https://openweathermap.org/api).

#### Methods

##### get_current_weather(city_name, unit = Unit.KELVIN)

It makes an http request (throught the [requests](http://2.python-requests.org/en/master/) package) to the OpenWeatherMap API to get the current weather forecast of the city you searched.

| Parameter | Description                                                                         | Required |
| --------- | ----------------------------------------------------------------------------------- | -------- |
| city_name | a string that represents the city you want to know the weather                      | Yes      |
| unit      | default unit is kelvin (You can leave it empty). See [Unit](#unit) for futher info. | No       |

This method returns a dictionary like the one below:

```
{
        'is_status_code_ok': True,
        'id': 2643743,
        'name': 'London',
        'country': 'GB',
        'forecast':{
            'main': 'Drizzle',
            'description': 'light intensity drizzle',
            'temperature': 280.32,
            'humidity': 81,
            'wind_speed': 4.1,
            'icon': '09d'
        }
}
```

For errors, see the [Errors](#errors) section.

##### get_days_weather(self, city_name, unit = Unit.KELVIN, days = Days.FIVE)

If you want to know the weather of a city for a maximum of 5 days (including the current day) you have to use this method.

| Parameter | Description                                                                          | Required |
| --------- | ------------------------------------------------------------------------------------ | -------- |
| city_name | a string that represents the city you want to know the weather                       | Yes      |
| unit      | default unit is kelvin (You can leave it empty). See [Unit](#unit) for futher info.  | No       |
| days      | default day is five [5] (You can leave it empty). See [Days](#Days) for futher info. | No       |

This method returns a dictionary like the one below (in this example the unit was metric and the days were two):

```
{
   'is_status_code_ok':True,
   'id':2643743,
   'name':'London',
   'country':'GB',
   'forecasts':[
      {
         'date':'28/05/2019',
         'temp_min':13,
         'temp_max':18,
         'weather':[
            {
               'time':'17:00:00',
               'main':'Clear',
               'description':'Clear sky',
               'temperature':17,
               'wind_speed':3.88,
               'icon':'01d'
            },
            {
               'time':'20:00:00',
               'main':'Clear',
               'description':'Clear sky',
               'temperature':16,
               'wind_speed':2.86,
               'icon':'01d'
            },
            {
               'time':'23:00:00',
               'main':'Rain',
               'description':'Light rain',
               'temperature':13,
               'wind_speed':0.68,
               'icon':'10n'
            }
         ]
      },
      {
         'date':'29/05/2019',
         'temp_min':10,
         'temp_max':18,
         'weather':[
            {
               'time':'02:00:00',
               'main':'Rain',
               'description':'Light rain',
               'temperature':11,
               'wind_speed':1.35,
               'icon':'10n'
            },
            {
               'time':'05:00:00',
               'main':'Clouds',
               'description':'Overcast clouds',
               'temperature':10,
               'wind_speed':1.26,
               'icon':'04n'
            },
            {
               'time':'08:00:00',
               'main':'Clouds',
               'description':'Broken clouds',
               'temperature':11,
               'wind_speed':1.21,
               'icon':'04d'
            },
            {
               'time':'11:00:00',
               'main':'Clouds',
               'description':'Scattered clouds',
               'temperature':15,
               'wind_speed':1.57,
               'icon':'03d'
            },
            {
               'time':'14:00:00',
               'main':'Clouds',
               'description':'Scattered clouds',
               'temperature':15,
               'wind_speed':4.3,
               'icon':'03d'
            },
            {
               'time':'17:00:00',
               'main':'Clouds',
               'description':'Broken clouds',
               'temperature':15,
               'wind_speed':4.64,
               'icon':'04d'
            },
            {
               'time':'20:00:00',
               'main':'Clouds',
               'description':'Broken clouds',
               'temperature':15,
               'wind_speed':3.7,
               'icon':'04d'
            },
            {
               'time':'23:00:00',
               'main':'Clouds',
               'description':'Overcast clouds',
               'temperature':14,
               'wind_speed':3.79,
               'icon':'04n'
            }
         ]
      }
   ]
}
```

For errors, see the [Errors](#errors) section.

### Errors

In case something goes wrong this dictionary is what is returned:

```
{
    'is_status_code_ok': False,
    'cod': '404',
    'message': 'city not found'
}
```

Common status code error:

| Code | Description                                                                       |
| ---- | --------------------------------------------------------------------------------- |
| 400  | Bad Request - city_name or API_KEY not set                                        |
| 401  | Invalid API key. Please see http://openweathermap.org/faq#error401 for more info. |
| 404  | city not found                                                                    |
| 429  | API key blocked                                                                   |
| 500  | internal server error                                                             |

#### Check the status code of your request

If you want to quickly check if your request was successful or not, just check the `is_status_code_ok` like:

```
w['is_status_code_ok']
```

If the response status code is less than 400 it's `True` otherwise it's `False`

## Built With

- [Python](https://python.org) (3.7)

## Version

> 1.0.1

Add install_requires to setup.py file.

> 1.0.0

Initial release. Include features like get the current weather of a city or get the weather of a city for more than one day.

## Author

> **Cosimo Matteini** - [devmatteini on github](https://github.com/devmatteini)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/devmatteini/forecastpy/blob/master/LICENSE) file for details
