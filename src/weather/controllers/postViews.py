import json
from django.http import JsonResponse
from ..middleware.authentication import authentication
from weather.controllers.API_KEY import API_KEY
from weatherapp.serializers import CurrentWeatherRequestSerializer, ForecastWeatherRequestSerializer
from ..middleware.loggingMechanism import logger
from .weatherApi import get_historical_weather_data, get_lat_lon, get_weather_current_response, get_weather_forecast_response
from rest_framework.response import Response
from datetime import datetime

def postCurrentWeatherView (request):
    serializer = CurrentWeatherRequestSerializer(data=request.data)

    authentication(request)

    if serializer.is_valid():

        location = serializer.validated_data['location']
            
        logger.info(f'POST request received with location={location}')
        logger.info('Request received: %s', request)
        
        # Get weather data for the location
        logger.info(f'Weather data retrieved for location={location}')
        weather_data = get_weather_current_response(location, API_KEY)
        return weather_data
    
    else:
        # Return a bad request response if the serializer is not valid
        logger.error('Invalid POST request received')
        return Response('Invalid POST request received, check your parameters', status=400)
    
def postForecastWeatherView(request):
    serializer = ForecastWeatherRequestSerializer(data=request.data)

    authentication(request)

    if serializer.is_valid():
        location = serializer.validated_data['location']
        days = serializer.validated_data['days']

        # Get weather data for the location
        weather_data = get_weather_forecast_response(location, days, API_KEY)

        logger.info('Weather forecast data retrieved: %s', weather_data)
        return JsonResponse(weather_data)
    
    else:
        # Return a bad request response if the serializer is not valid
        logger.error('Invalid POST request received')
        return Response('Invalid POST request received, check your parameters', status=400)
    

def postHistoryWeatherView(request):
    data = json.loads(request.body)
    location = data.get('location')

    logger.info(f"Received historical weather request for location: {location}")
        
    authentication(request)
        
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