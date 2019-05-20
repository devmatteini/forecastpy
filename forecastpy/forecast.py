import requests
import json

class Unit():
    KELVIN = ''
    METRIC = 'metric'
    FAHRENHEIT = 'imperial'

class Weather:
    
    API_KEY = None

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_current_weather(self, city_name, unit = Unit.KELVIN):
        if self.API_KEY is None or city_name is None or city_name is '':
            return {
                'is_status_code_ok': False,
                'cod': '400', 
                'message': 'Bad Request - city_name or API_KEY cannot be None or empty'
            }

        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'.format(city_name, unit, self.API_KEY)
        
        res = requests.get(url)
        data = json.loads(res.text)

        # Status code higher than 400 - see docs for futher details on status code errors
        if not res:
            data['is_status_code_ok'] = False
            return data;

        # Status code between 200 and 400
        return {
                'is_status_code_ok': True,
                'id': data['id'],
                'name': data['name'],
                'country': data['sys']["country"],
                'forecast':{
                    'main': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'icon': data['weather'][0]['icon']
                }
            }