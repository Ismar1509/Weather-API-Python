from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weatherapp.serializers import CurrentWeatherRequestSerializer
from ..middleware.errors import bad_request_error, not_found_error, server_error
from .weatherApi import get_weather_current_response
import requests
from ..middleware.loggingMechanism import logger
from .API_KEY import API_KEY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get', 
    operation_summary='Get current weather', 
    operation_description='Get current weather for a specific location',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            required=True
        ),
    ]
)

@swagger_auto_schema(
    method='post',
    operation_summary='Create new weather entry',
    operation_description='Create a new weather entry for a specific location',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'location': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The name of the location'
            ),
        },
        required='location'
    )
)

@api_view(['GET', 'POST'])
def current_weather(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        logger.info(f'GET request received with location={location}')
        logger.info('Request received: %s', request)
        
        if not location:
            logger.error('Location parameter not provided')
            return bad_request_error('Location is required')
        weather_data = get_weather_current_response(location, API_KEY)
        
        logger.info(f'Weather data retrieved for location={location}, %s', weather_data)
        return Response(weather_data)
    
    elif request.method == 'POST':
        serializer = CurrentWeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            logger.info(f'POST request received with location={location}')
            logger.info('Request received: %s', request)
            # Get weather data for the location
            logger.info(f'Weather data retrieved for location={location}')
            weather_data = get_weather_current_response(location, API_KEY)
            return Response(weather_data)
        else:
            # Return a bad request response if the serializer is not valid
            logger.error('Invalid POST request received')
            return Response(serializer.errors, status=400)