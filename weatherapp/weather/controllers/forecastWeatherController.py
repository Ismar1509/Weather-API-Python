from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weatherapp.serializers import ForecastWeatherRequestSerializer
from .weatherApi import get_weather_forecast_response
from ..middleware.errors import bad_request_error
import requests, json
from .API_KEY import API_KEY
from ..middleware.loggingMechanism import logger

@api_view(['GET', 'POST'])
def weather_forecast(request):
    logger.info('Request received: %s', request)

    if request.method == 'GET':
        location = request.GET.get('location', '')
        days = request.GET.get('days', '')
        if not location:
            logger.error('Location is required')
            return bad_request_error('Location is required')
        if not days:
            logger.error('Days are required')
            return bad_request_error('Days are required')
        if not days.isdigit():
            logger.error('Days must not be negative number')
            return bad_request_error('Days must not be negative number')
        days = int(days)
        if days < 1 or days > 7:
            logger.error('Days must be between 1 and 7')
            return bad_request_error('Days must be between 1 and 7')
        weather_data = get_weather_forecast_response(location, days, API_KEY)
        logger.info('Weather forecast data retrieved: %s', weather_data)
        return Response(weather_data)
    
    elif request.method == 'POST':
        serializer = ForecastWeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            days = serializer.validated_data['days']
            # Get weather data for the location
            weather_data = get_weather_forecast_response(location, days, API_KEY)
            logger.info('Weather forecast data retrieved: %s', weather_data)
            return Response(weather_data)
        else:
            # Return a bad request response if the serializer is not valid
            logger.error('Invalid data: %s', serializer.errors)
            return Response(serializer.errors, status=400)

