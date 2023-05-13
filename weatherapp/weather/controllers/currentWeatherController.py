from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weatherapp.serializers import CurrentWeatherRequestSerializer
from .errors import bad_request_error, not_found_error, server_error
from .weatherApi import get_weather_current_response
import requests

API_KEY = ''


@api_view(['GET', 'POST'])
def current_weather(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        if not location:
            return bad_request_error('Location is required')
        weather_data = get_weather_current_response(location, API_KEY)
        return Response(weather_data)
    
    elif request.method == 'POST':
        serializer = CurrentWeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            # Get weather data for the location
            weather_data = get_weather_current_response(location, API_KEY)
            return Response(weather_data)
        else:
            # Return a bad request response if the serializer is not valid
            return Response(serializer.errors, status=400)