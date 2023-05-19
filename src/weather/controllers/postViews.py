import json
from django.http import JsonResponse
from ..middleware.authentication import authentication
from weather.controllers.API_KEY import API_KEY
from weatherapp.serializers import CurrentWeatherRequestSerializer, ForecastWeatherRequestSerializer
from ..middleware.loggingMechanism import logger
from .weatherApi import get_historical_weather_data, get_lat_lon, get_weather_current_response, get_weather_forecast_response
from rest_framework.response import Response
from datetime import datetime

#Funcionality of POST method for current weather
def postCurrentWeatherView (request):

    #Validate and parse data in request through serializer
    serializer = CurrentWeatherRequestSerializer(data=request.data)

    #Call function to authenticate user
    authentication(request)

    #If serializer properly validated data, proceed
    if serializer.is_valid():

        #Extract location parameter from validated data
        location = serializer.validated_data['location']
        
        #Return some info to log files
        logger.info(f'POST request received with location={location}')
        logger.info('Request received: %s', request)
        
        # Get weather data for the current weather
        logger.info(f'Weather data retrieved for location={location}')
        weather_data = get_weather_current_response(location, API_KEY)
        return weather_data
    
    else:
        # Return a bad request response if the serializer is not valid
        logger.error('Invalid POST request received')
        return Response('Invalid POST request received, check your parameters', status=400)

#Funcionality of POST method for forecast weather
def postForecastWeatherView(request):

    #Validate and parse data in request through serializer
    serializer = ForecastWeatherRequestSerializer(data=request.data)

    #Call function to authenticate user
    authentication(request)

    #If serializer properly validated data, proceed
    if serializer.is_valid():

        #Extract data
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
    
#Funcionality of POST method for history weather
def postHistoryWeatherView(request):

    # Parse the request body as JSON and extract location
    data = json.loads(request.body)
    location = data.get('location')

    #Some info for log file
    logger.info(f"Received historical weather request for location: {location}")

    #Call function to authenticate user    
    authentication(request)
        
    # Retrieve latitude and longitude for the location    
    lat_lon = get_lat_lon(location)

    if lat_lon is None:
        # Failed to retrieve latitude and longitude
        logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
        return JsonResponse({'error': 'Failed to retrieve latitude and longitude for location'})

    # Extract start_date and end_date from the request data    
    lat, lon = lat_lon
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    # Convert start_date and end_date to timestamps    
    start_date = int(datetime.fromisoformat(start_date_str).timestamp())
    end_date = int(datetime.fromisoformat(end_date_str).timestamp())

    #Fetch weather data from function    
    weather_data = get_historical_weather_data(lat, lon, start_date, end_date, API_KEY)

    # Successfully retrieved weather data    
    if weather_data:
        logger.info(f"Retrieved historical weather data for location: {location}")
        return JsonResponse({'weather_data': weather_data})
    
    else:
        # Failed to retrieve weather data
        logger.error(f"Failed to retrieve weather data for location: {location}")
        return JsonResponse({'error': 'Failed to retrieve weather data'})