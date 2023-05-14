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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get', 
    operation_summary='Get forecast weather', 
    operation_description='Get forecast weather for a specific location',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            required=True
        ),
        openapi.Parameter(
            name='days',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='The number of days to get the weather for',
            required=True
        ),
    ]
)

#@swagger_auto_schema(
#    method='post',
#    operation_summary='Create forecast weather entry',
#    operation_description='Create a forecast weather entry for a specific location and number of days',
#    request_body=openapi.Schema(
#        type=openapi.TYPE_OBJECT,
#        properties={
#            'location': openapi.Schema(
#                type=openapi.TYPE_STRING,
#                description='The name of the location'
#            ),
#            'days' : openapi.Schema(
#                type = openapi.TYPE_INTEGER,
#                description='Number of days for location'
#            )
#        },
#        required=['location', 'days']
#    )
#)

#@api_view(['GET', 'POST'])
#if POST is also needed just uncomment comment above, and comment one below, other comments should also be uncommented
@api_view(['GET'])
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
    
    #elif request.method == 'POST':
    #    serializer = ForecastWeatherRequestSerializer(data=request.data)
    #    if serializer.is_valid():
    #        location = serializer.validated_data['location']
    #        days = serializer.validated_data['days']
    #        # Get weather data for the location
    #        weather_data = get_weather_forecast_response(location, days, API_KEY)
    #        logger.info('Weather forecast data retrieved: %s', weather_data)
    #        return Response(weather_data)
    #    else:
    #        # Return a bad request response if the serializer is not valid
    #        logger.error('Invalid data: %s', serializer.errors)
    #        return Response(serializer.errors, status=400)
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})

