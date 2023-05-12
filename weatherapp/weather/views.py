from django.shortcuts import render
import requests
from django.http import JsonResponse

API_KEY = ''


def current_weather(request, location):
    # Set up OpenWeatherMap API parameters
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'

    # Make API request to OpenWeatherMap
    response = requests.get(api_url)
    data = response.json()

    # Return weather data as JSON response
    return JsonResponse(data, safe=False)

def weather_forecast(request, location):
    # Set up OpenWeatherMap API parameters
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'

    # Make API request to OpenWeatherMap
    response = requests.get(api_url)
    data = response.json()

    # Return forecast data as JSON response
    return JsonResponse(data, safe=False)