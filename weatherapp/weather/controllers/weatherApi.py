import json
import requests
from ..middleware.errors import not_found_error, server_error, bad_request_error
import time, datetime
from .API_KEY import API_KEY
from cache_memoize import cache_memoize
from django.utils import timezone
import pytz
from datetime import datetime
from ..models.responseBody import responseBodyCurrent, responseBodyForecast, responseBodyHistorical

@cache_memoize(300)  # cache for 5 minutes
def get_weather_current_response(location, API_KEY):
    print(f"Fetching weather data for {location}")

    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric')
    if response.status_code == 200:
        #data = response.json()
        data = response.json()
        weather_data = responseBodyCurrent(data)
        return weather_data
    else:
        return {'error': 'Unable to fetch weather data.'}

@cache_memoize(300)  # cache for 5 minutes
def get_weather_forecast_response(location, days, API_KEY):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = responseBodyForecast(data)

        last_refresh_time = datetime.now(pytz.utc)
        last_refresh_time_str = last_refresh_time.astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")

        return {'weather_data': weather_data, 'last_refresh_time': last_refresh_time_str}
    else:
        return {'error': 'Unable to fetch forecast weather data.'}    

def get_lat_lon(location):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) == 0:
            return None
        lat = data[0]['lat']
        lon = data[0]['lon']
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return None
        return lat, lon
    else:
        return None

@cache_memoize(300)  # cache for 5 minutes
def get_historical_weather_data(lat, lon, start_date, end_date, API_KEY):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&appid={API_KEY}&start={start_date}&end={end_date}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = responseBodyHistorical(data)

        last_refresh_time = datetime.now(pytz.utc)
        last_refresh_time_str = last_refresh_time.astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")

        return {'weather_data': weather_data, 'last_refresh_time': last_refresh_time_str}
    else:
        return {'error': 'Unable to fetch historical weather data.'}





    










