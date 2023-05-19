import requests
from ..middleware.errors import not_found_error, server_error, bad_request_error
import  datetime
from .API_KEY import API_KEY
from cache_memoize import cache_memoize
import pytz
from datetime import datetime
from ..models.responseBody import responseBodyCurrent, responseBodyForecast, responseBodyHistorical

#Decorator for caching
@cache_memoize(300)  # cache for 5 minutes

#Function for fetching response for current weather
def get_weather_current_response(location, API_KEY):

    #Fetch data
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric')
    
    #If fetching is successful
    if response.status_code == 200:

        #Parse JSON response
        data = response.json()

        #Call response body function and pass data to get proper info about weather
        weather_data = responseBodyCurrent(data)

        #Create object that represents current date and time for UTC timezone
        last_refresh_time = datetime.now(pytz.utc)

        #Convert UTC timezone to location of Sarajevu in Europe and format the time
        last_refresh_time_str = last_refresh_time.astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")

        return {'weather_data': weather_data, 'last_refresh_time': last_refresh_time_str, 'provider' : 'OpenWeatherMap'}
    else:
        return {'error': 'Unable to fetch weather data, check the parameters you provided'}

#Decorator for caching
@cache_memoize(300)  # cache for 5 minutes

#Function for fetching response for forecast weather
def get_weather_forecast_response(location, days, API_KEY):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'
    
    #Fetch data
    response = requests.get(url)

    #If it is successfull, parse JSON response, and call response body with data being passed
    if response.status_code == 200:
        data = response.json()
        weather_data = responseBodyForecast(data)

        #Create object that represents current date and time for UTC timezone
        last_refresh_time = datetime.now(pytz.utc)

        #Convert UTC timezone to location of Sarajevu in Europe and format the time
        last_refresh_time_str = last_refresh_time.astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")

        return {'weather_data': weather_data, 'last_refresh_time': last_refresh_time_str, 'provider' : 'OpenWeatherMap'}
    else:
        return {'error': 'Unable to fetch weather data, check the parameters you provided'}    

#Function that uses provided location to find latitude and longitude of location
def get_lat_lon(location):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    
    #Fetch data
    response = requests.get(url)
    
    #If it is successfull, parse JSON response 
    if response.status_code == 200:
        data = response.json()

        #If no data, return None, take first latitude and longitude from data that was given as response
        if len(data) == 0:
            return None
        lat = data[0]['lat']
        lon = data[0]['lon']

        #Ensure they fit valid range and return them
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return None
        return lat, lon
    else:
        return None

#Decorator for caching
@cache_memoize(300)  # cache for 5 minutes

#Function for fetching response for historical weather
def get_historical_weather_data(lat, lon, start_date, end_date, API_KEY):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&appid={API_KEY}&start={start_date}&end={end_date}&units=metric"
    
    #Fetch the data
    response = requests.get(url)

    #If fetching was successful, parse JSON response and call response body with data passed as argument
    if response.status_code == 200:
        data = response.json()
        weather_data = responseBodyHistorical(data)

        #Create object for time using UTC timezone and convert it to Europe/Sarajevo time
        last_refresh_time = datetime.now(pytz.utc)
        last_refresh_time_str = last_refresh_time.astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")

        return {'weather_data': weather_data, 'last_refresh_time': last_refresh_time_str, 'provider' : 'OpenWeatherMap'}
    else:
        return {'error': 'Unable to fetch historical weather data.'}





    










