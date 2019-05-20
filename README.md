# ForecastPy

A python module to interact with the OpenWeatherAPI in a simple and fast way.

## Getting Started

### Installing

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install WeatherPy.

```
pip install forecastpy
```

## Usage

```
from forecast import Weather, Unit

# Init Weather object with your open weather api key
weather = Weather('YOUR_API_KEY')

# Get current weather from a city name
w = weather.get_current_weather('CITY_NAME',Unit.METRIC)
```

## Documentation

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

### Weather

Weather is the class you'll need to use to interact with the open weather api.
It requires the open weather api key as its only parameter when you have to initialize it.

#### Methods

##### get_current_weather(city_name, unit = Unit.KELVIN)

It makes an http request (throught the [requests](http://2.python-requests.org/en/master/) module) to the OpenWeatherMap API to get the current weather forecast of the city you searched.

| Parameter | Description |
| --------- | ------------|
| city_name | a string that represents the city you want to know the weather|
| unit      | default unit is kelvin (You can leave the unit parameter empty). If you want to change the unit see the Unit class section above |

This method returns a dictionary like the one below:

```
{
        is_status_code_ok: True,
        id: 2643743,
        name: 'London',
        country: 'GB',
        forecast:{
            main: 'Drizzle',
            description: 'light intensity drizzle',
            temperature: 280.32,
            humidity: 81,
            wind_speed: 4.1,
            icon: '09d'
        }
}
```

In case something goes wrong this dictionary is what is returned:
```
{
    'cod': '404', 
    'message': 'city not found'
}
```

Common status code error:

| Code | Description |
|------|-------------|
|400 | Bad Request - city_name or API_KEY not set|
| 401 | Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.|
|404 | city not found|
|429 |  API key blocked |
|500 | internal server error|

##### Check The Status Code of your request
If you want to quickly check if your request was successful or not just check the `is_status_code_ok` like:
```
w['is_status_code_ok']
```
If the response code is between 200 and 400 it's `True` otherwise it's `False`

## Built With

- [Python](https://python.org)

## Versioning

I use [Git](https://git-scm.com/) for versioning. For the versions available, see the [tags on this repository](https://github.com/devmatteini/forecastpy).

## Author

- **Cosimo Matteini** - [devmatteini on github](https://github.com/devmatteini)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/devmatteini/forecastpy/blob/master/LICENSE) file for details
