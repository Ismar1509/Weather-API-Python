import json
import requests
from .errors import not_found_error, server_error

API_KEY = ''

def get_forecast_weather(location, days, API_KEY):
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric&cnt={days * 8}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return not_found_error()
    else:
        error_message = f'Error {response.status_code}: {response.json()["message"]}'
        return server_error(error_message)
    
def get_current_weather(location, API_KEY):
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return not_found_error()
        else:
            error_message = f'Error {response.status_code}: {response.json()["message"]}'
            return server_error(error_message)

    except TypeError as e:
        return server_error(f'TypeError: ')

def get_weather_forecast_response(location, days, API_KEY):
    weather_data = get_forecast_weather(location, days, API_KEY)
    if 'error' in weather_data:
        return weather_data
    else:
        return json.loads(json.dumps(weather_data))

def get_weather_current_response(location, API_KEY):
    weather_data = get_current_weather(location,  API_KEY)
    if 'error' in weather_data:
        return weather_data
    else:
        return json.loads(json.dumps(weather_data))

