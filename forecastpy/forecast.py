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

    API_KEY = None

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_current_weather(self, city_name, unit=Unit.KELVIN):
        if (self.API_KEY is None or self.API_KEY is '') or (city_name is None or city_name is ''):
            return {
                'is_status_code_ok': False,
                'cod': '400',
                'message': 'Bad Request - city_name or API_KEY cannot be None or empty'
            }

        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'.format(
            city_name, unit, self.API_KEY)

        res = requests.get(url)
        data = json.loads(res.text)

        # Status code higher than 400 - see docs for futher details on status code errors
        if not res.ok:
            data['is_status_code_ok'] = False
            return data

        # Status code is less than 400
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
        if (self.API_KEY is None or self.API_KEY is '') or (city_name is None or city_name is ''):
            return {
                'is_status_code_ok': False,
                'cod': '400',
                'message': 'Bad Request - city_name or API_KEY cannot be None or empty'
            }

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

        forecasts['forecasts'] = self.__make_forecasts(data['list'], days)

        return forecasts

    def __make_forecasts(self, list, days):
        first_forecast_date = datetime.fromtimestamp(list[0]['dt'])

        # Determine how much hours left till midnight to get how much elements has the current day since it can change during the day
        start = 0
        end = round((24 - first_forecast_date.hour) / 3)

        forecasts = []

        for i in range(days):
            # Dictionary that holds all the forecasts for a single day
            day = self.__make_day(list, start, end)
            forecasts.append(day)

            # Increment range to go to the next day
            start = end + 1
            end = start + 7

        return forecasts

    def __make_day(self, list, start, end):
        day = {
            'date': datetime.fromtimestamp(list[start]['dt']).strftime('%d/%m/%Y'),
            'temp_min': None,
            'temp_max': None,
            'weather': []
        }

        # List of all the forecasts of the day (every three hours)
        w = []
        min = list[0]['main']['temp_min']
        max = list[0]['main']['temp_max']

        for i in range(start, end + 1):
            item = list[i]

            # Determine min and max temperature of the day
            if min > item['main']['temp_min']:
                min = item['main']['temp_min']
            if max < item['main']['temp_max']:
                max = item['main']['temp_max']

            temp = {
                'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M:%S'),
                'main': item['weather'][0]['main'].capitalize(),
                'description': item['weather'][0]['description'].capitalize(),
                'temperature': int(round(item['main']['temp'])),
                'wind_speed': item['wind']['speed'],
                'icon': item['weather'][0]['icon']
            }
            w.append(temp)

        day['temp_min'] = int(round(min))
        day['temp_max'] = int(round(max))
        day['weather'] = w
        return day
