from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest, JsonResponse
from weatherapp.serializers import HistoryWeatherRequestSerializer
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from ..middleware.errors import  retrieve_location_error
import requests
from datetime import datetime, timedelta
import json, os

from ..middleware.loggingMechanism import logger
from .API_KEY import API_KEY

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

def get_historical_weather_data(lat, lon, start_date, end_date):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&appid={API_KEY}&start={start_date}&end={end_date}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        for hour in data['list']:
            weather = {
                'timestamp': hour['dt'],
                'temperature': hour['main']['temp'],
                'humidity': hour['main']['humidity'],
                'wind_speed': hour['wind']['speed'],
                'description': hour['weather'][0]['description']
            }
            weather_data.append(weather)
        return weather_data
    else:
        return None

@csrf_exempt
def historical_weather(request):
    if request.method == 'GET':
        location = request.GET.get('location')

        logger.info(f"Received historical weather request for location: {location}")

        if location is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return retrieve_location_error()
        
        lat_lon = get_lat_lon(location)
        if lat_lon is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve latitude and longitude for location'})
        
        lat, lon = lat_lon
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str is None:
            logger.error(f"Failed to retrieve start date: {location}")
            return JsonResponse({'error': 'Failed to retrieve start date'})
        
        if end_date_str is None:
            logger.error(f"Failed to retrieve end date: {location}")
            return JsonResponse({'error': 'Failed to retrieve end date'})
        
        start_date = int(datetime.fromisoformat(start_date_str).timestamp())
        end_date = int(datetime.fromisoformat(end_date_str).timestamp())
        
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date)
        
        if weather_data:
            logger.info(f"Retrieved historical weather data for location: {location}")
            return JsonResponse({'weather_data': weather_data})
        else:
            logger.error(f"Failed to retrieve weather data for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve weather data'})
    elif request.method == 'POST':
        data = json.loads(request.body)
        location = data.get('location')

        logger.info(f"Received historical weather request for location: {location}")
        
        
        lat_lon = get_lat_lon(location)
        if lat_lon is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve latitude and longitude for location'})
        
        lat, lon = lat_lon
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        
        start_date = int(datetime.fromisoformat(start_date_str).timestamp())
        end_date = int(datetime.fromisoformat(end_date_str).timestamp())
        
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date)
        
        if weather_data:
            logger.info(f"Retrieved historical weather data for location: {location}")
            return JsonResponse({'weather_data': weather_data})
        else:
            logger.error(f"Failed to retrieve weather data for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve weather data'})
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})




