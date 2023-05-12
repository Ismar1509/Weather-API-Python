from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import requests

API_KEY = '915b407319f462c2ec5f309b6d4df5f2'

def weather_history(request, location):
    # Set up OpenWeatherMap API parameters
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'

    # Make API request to OpenWeatherMap
    response = requests.get(api_url)
    data = response.json()

    # Return weather data as JSON response
    return JsonResponse(data, safe=False)