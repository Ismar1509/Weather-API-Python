from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest, JsonResponse
from weatherapp.serializers import ForecastWeatherRequestSerializer
from rest_framework.response import Response
import requests

API_KEY = ''

def get_forecast_weather(location):
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = f'Error {response.status_code}: {response.json()["message"]}'
        raise Exception(error_message)

@api_view(['GET', 'POST'])
def weather_forecast(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        if not location:
            return JsonResponse({'error': 'Location is required'}, status=400)
        weather_data = get_forecast_weather(location)
        return JsonResponse(weather_data, safe=False)
    
    elif request.method == 'POST':
        serializer = ForecastWeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            # Get weather data for the location
            weather_data = get_forecast_weather(location)
            # Return the weather data as a JSON response
            return Response(weather_data)
        else:
            # Return a bad request response if the serializer is not valid
            return Response(serializer.errors, status=400)
