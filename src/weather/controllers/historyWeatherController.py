import base64
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpRequest, HttpResponse, JsonResponse
from weatherapp.serializers import HistoryWeatherRequestSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from ..middleware.errors import  retrieve_location_error
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
from ..swagger.historyWeatherSwagger import history_weather_get_swagger, history_weather_post_swagger

@history_weather_get_swagger
@history_weather_post_swagger
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




