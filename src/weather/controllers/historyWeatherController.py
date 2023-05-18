import base64
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpRequest, HttpResponse, JsonResponse
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
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


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
            example="Sarajevo",
            required=True
        ),
        openapi.Parameter(
            name='start_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The start date for historical data (YYYY-MM-DD)',
            example="2022-01-01",
            required=True
        ),
        openapi.Parameter(
            name='end_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The end date for historical data (YYYY-MM-DD)',
            example="2022-01-05",
            required=True
        ),
    ]
)


@swagger_auto_schema(
    method='post',
    operation_summary='Create historical data for weather entry',
    operation_description='Create a historical weather data for a specific location and range in date',
    manual_parameters=[
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description='Authorization header with Basic Authentication',
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'location': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The name of the location',
                example="Sarajevo"
            ),
            'start_date' : openapi.Schema(
                type = openapi.TYPE_STRING,
                description='Start date (YYYY-MM-DD)',
                example='2023-01-01'
            ),
            'end_date' : openapi.Schema(
                type = openapi.TYPE_STRING,
                description='End date (YYYY-MM-DD)',
                example='2023-01-05'
            )
        },
        required=['location', 'start_date', 'end_date']
    ),
    responses={
        200: 'A successful response',
        400: 'Bad request',
        401: 'Unauthorized',
        500: 'Internal server error',
    }
)



@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        location = data.get('location')

        logger.info(f"Received historical weather request for location: {location}")
        
        if 'Authorization' not in request.headers:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Basic realm="API"'
            return response

    # Extract and decode the Authorization header
        auth_header = request.headers['Authorization']
        if not auth_header.startswith('Basic '):
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Basic realm="API"'
            return response

        encoded_credentials = auth_header.split(' ')[1]
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = credentials.split(':')

         # Log or print the username and password
        logger.info(f"Username: {username}")
        logger.info(f"Password: {password}")


    # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is None:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = 'Basic realm="API"'
            return response
        
        lat_lon = get_lat_lon(location)
        if lat_lon is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve latitude and longitude for location'})
        
        lat, lon = lat_lon
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        
        start_date = int(datetime.fromisoformat(start_date_str).timestamp())
        end_date = int(datetime.fromisoformat(end_date_str).timestamp())
        
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date, API_KEY)
        
        if weather_data:
            logger.info(f"Retrieved historical weather data for location: {location}")
            return JsonResponse({'weather_data': weather_data})
        else:
            logger.error(f"Failed to retrieve weather data for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve weather data'})
        
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})




