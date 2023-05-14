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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .weatherApi import get_lat_lon, get_historical_weather_data


@swagger_auto_schema(
    method='get', 
    operation_summary='Get historical data for weather', 
    operation_description='Get historical weather data for a specific location for range of dates',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            required=True
        ),
        openapi.Parameter(
            name='start_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The start date for historical data (YYYY-MM-DD)',
            required=True
        ),
        openapi.Parameter(
            name='end_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The end date for historical data (YYYY-MM-DD)',
            required=True
        ),
    ]
)


#@swagger_auto_schema(
#    method='post',
#    operation_summary='Create historical data for weather entry',
#    operation_description='Create a historical weather data for a specific location and range in date',
#    request_body=openapi.Schema(
#        type=openapi.TYPE_OBJECT,
#        properties={
#            'location': openapi.Schema(
#                type=openapi.TYPE_STRING,
#                description='The name of the location'
#            ),
#            'start_date' : openapi.Schema(
#                type = openapi.TYPE_STRING,
#                description='Start date (YYYY-MM-DD)'
#            ),
#            'end_date' : openapi.Schema(
#                type = openapi.TYPE_STRING,
#                description='End date (YYYY-MM-DD)'
#            )
#        },
#        required=['location', 'start_date', 'end_date']
#    )
#)

@csrf_exempt
#@api_view(['GET', 'POST'])
#if POST is also needed just uncomment comment above, and comment one below, other comments should also be uncommented
@api_view(['GET'])
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
        
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date, API_KEY)
        
        if weather_data:
            logger.info(f"Retrieved historical weather data for location: {location}")
            return JsonResponse({'weather_data': weather_data})
        else:
            logger.error(f"Failed to retrieve weather data for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve weather data'})
    #elif request.method == 'POST':
        #data = json.loads(request.body)
        #location = data.get('location')

        #logger.info(f"Received historical weather request for location: {location}")
        
        
        #lat_lon = get_lat_lon(location)
        #if lat_lon is None:
        #    logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
        #    return JsonResponse({'error': 'Failed to retrieve latitude and longitude for location'})
        
        #lat, lon = lat_lon
        #start_date_str = data.get('start_date')
        #end_date_str = data.get('end_date')
        
        #start_date = int(datetime.fromisoformat(start_date_str).timestamp())
        #end_date = int(datetime.fromisoformat(end_date_str).timestamp())
        
        #weather_data = get_historical_weather_data(lat, lon, start_date, end_date)
        
        #if weather_data:
        #    logger.info(f"Retrieved historical weather data for location: {location}")
        #    return JsonResponse({'weather_data': weather_data})
        #else:
        #    logger.error(f"Failed to retrieve weather data for location: {location}")
        #    return JsonResponse({'error': 'Failed to retrieve weather data'})
        #
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})




