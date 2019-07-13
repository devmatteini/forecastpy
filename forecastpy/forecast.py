import requests
import json
from datetime import datetime


class Unit():
    KELVIN = ''
    METRIC = 'metric'
    FAHRENHEIT = 'imperial'


class Days():
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Weather:

    def __init__(self, API_KEY):
        if API_KEY is None:
            raise TypeError(
                'Invalid argument: [NoneType] - must be a [str]')

        self.API_KEY = API_KEY

    def get_current_weather(self, city_name, unit=Unit.KELVIN):
        self.__check_request(city_name)

        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'.format(
            city_name, unit, self.API_KEY)

        res = requests.get(url)
        data = json.loads(res.text)

        # Status code higher than 400 - see docs for futher details on status code errors
        if not res.ok:
            data['is_status_code_ok'] = False
            return data

        return {
            'is_status_code_ok': True,
            'id': data['id'],
            'name': data['name'],
            'country': data['sys']["country"],
            'forecast': {
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'temperature': int(round(data['main']['temp'])),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon']
            }
        }

    def get_days_weather(self, city_name, unit=Unit.KELVIN, days=Days.FIVE):
        self.__check_request(city_name)

        url = 'https://api.openweathermap.org/data/2.5/forecast/?q={}&units={}&appid={}'.format(
            city_name, unit, self.API_KEY)

        res = requests.get(url)
        data = json.loads(res.text)

        # Status code higher than 400 - see docs for futher details on status code error
        if not res.ok:
            data["is_status_code_ok"] = False
            return data

        # Status code is less than 400
        forecasts = {
            'is_status_code_ok': True,
            'id': data['city']['id'],
            'name': data['city']['name'],
            'country': data['city']['country'],
            'forecasts': []
        }

        forecasts['forecasts'] = self.__get_forecasts(data['list'], days)

        return forecasts

    def __get_forecasts(self, list, days):
        first_forecast_date_hour = datetime.fromtimestamp(
            list[0]['dt']).hour

        # Determine how much hours left till midnight to get how much elements
        # has the current day since it can change during the day
        # based on the time of the request
        date_range = {
            'start': 0,
            'end': round((24 - first_forecast_date_hour) / 3)
        }

        forecasts = [self.__get_day(list, date_range) for i in range(days)]

        return forecasts

    def __get_day(self, list, date_range):
        day = self.__build_day_weather(list, date_range)

        date_range['start'] = date_range['end'] + 1
        date_range['end'] = date_range['start'] + 7

        return day

    def __build_day_weather(self, list, date_range):
        start = date_range['start']
        end = date_range['end']

        day = {
            'date': datetime.fromtimestamp(list[start]['dt']).strftime('%d/%m/%Y'),
            'temp_min': None,
            'temp_max': None,
            'weather': []
        }

        temperature_range = {
            'min': list[0]['main']['temp_min'],
            'max': list[0]['main']['temp_max']
        }

        # List of all the forecasts of the day (every three hours)
        day['weather'] = [self.__get_day_weather_info(
            list[i], temperature_range) for i in range(start, end + 1)]

        day['temp_min'] = int(round(temperature_range['min']))
        day['temp_max'] = int(round(temperature_range['max']))

        return day

    def __get_day_weather_info(self, current, temperature_range):
        temperature_range['min'] = current['main']['temp_min'] if temperature_range[
            'min'] > current['main']['temp_min'] else temperature_range['min']

        temperature_range['max'] = current['main']['temp_max'] if temperature_range[
            'max'] < current['main']['temp_max'] else temperature_range['max']

        return {
            'time': datetime.fromtimestamp(current['dt']).strftime('%H:%M:%S'),
            'main': current['weather'][0]['main'].capitalize(),
            'description': current['weather'][0]['description'].capitalize(),
            'temperature': int(round(current['main']['temp'])),
            'wind_speed': current['wind']['speed'],
            'icon': current['weather'][0]['icon']
        }

    def __check_request(self, city_name):
        if (self.API_KEY is None or self.API_KEY is '') or (city_name is None or city_name is ''):
            return {
                'is_status_code_ok': False,
                'cod': '400',
                'message': 'Bad Request - city_name or API_KEY cannot be None or empty'
            }
