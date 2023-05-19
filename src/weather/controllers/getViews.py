from ..middleware.handleNoEntry import handle_no_entry
from django.http import JsonResponse
from ..middleware.errors import bad_request_error, retrieve_location_error
from ..middleware.loggingMechanism import logger
from ..controllers.API_KEY import API_KEY
from .weatherApi import get_historical_weather_data, get_lat_lon, get_weather_current_response, get_weather_forecast_response
from ..middleware.authentication import authentication
from rest_framework.response import Response
from datetime import datetime

#Function to handle authentication and conditions/errors that could occur
#Function calls response function to obtain current weather data
def getCurrentWeatherView (request):
        
        #The function starts by calling the authentication function to authenticate the user based on the request headers.
        authentication(request)

        #Obtain info for location from request
        location = request.GET.get('location', '')
    	
        #Information to be store in log files
        logger.info(f'GET request received with location={location}')
        logger.info('Request received: %s', request)

        #If there is no location provided, return error
        if not location:
            logger.error('Location parameter not provided')
            return handle_no_entry('Location is required')
        
        #Gather data from response function
        weather_data = get_weather_current_response(location, API_KEY)
        logger.info(f'Weather data retrieved for location={location}, %s', weather_data)
        return Response(weather_data)

#Function to handle authentication and conditions/errors that could occur
#Function calls response function to obtain forecast weather data
def getForecastWeatherView(request):
        
        #The function starts by calling the authentication function to authenticate the user based on the request headers.
        authentication(request)

        #Information to be store in log files
        logger.info('Request received: %s', request)

        #Obtain info for location and days from request
        location = request.GET.get('location', '')
        days = request.GET.get('days', '')

        #If no location is entered, raise error
        if not location:
            logger.error('Location is required')
            return handle_no_entry('Location is required')
        
        #If no days parameter is entered, raise error
        if not days:
            logger.error('Days are required')
            return bad_request_error('Days are required')
        
        #If days are negative, raise error
        if not days.isdigit():
            logger.error('Days must not be negative number')
            return bad_request_error('Days must not be negative number')
        
        days = int(days)

        #If days are not in one week range, raise error
        if days < 1 or days > 7:
            logger.error('Days must be between 1 and 7')
            return bad_request_error('Days must be between 1 and 7')
        
        #Gather data from response function
        weather_data = get_weather_forecast_response(location, days, API_KEY)
        logger.info('Weather forecast data retrieved: %s', weather_data)
        return Response(weather_data)

#Function to handle authentication and conditions/errors that could occur
#Function calls response function to obtain historical weather data
def getHistoryWeatherView(request):

        #The function starts by calling the authentication function to authenticate the user based on the request headers.
        authentication(request)

        #Obtain info for location from request
        location = request.GET.get('location')
        logger.info(f"Received historical weather request for location: {location}")

        #If no location is entered, raise error
        if location is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return retrieve_location_error()
        
        #Get latitude and longitude from function
        lat_lon = get_lat_lon(location)

        #If there is no latitude and longitude returned, raise error
        if lat_lon is None:
            logger.error(f"Failed to retrieve latitude and longitude for location: {location}")
            return Response({'error': 'Failed to retrieve latitude and longitude for location'})
        
        #Assign latitude and longitude and fetch data for start and end date
        lat, lon = lat_lon
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        #If there is no start date, raise error
        if start_date_str is None:
            logger.error(f"Failed to retrieve start date: {location}")
            return Response({'error': 'Failed to retrieve start date'})
        
        #If there is no end date, raise error
        if end_date_str is None:
            logger.error(f"Failed to retrieve end date: {location}")
            return Response({'error': 'Failed to retrieve end date'})
        
        #Convert datetime into unixtimestamp
        start_date = int(datetime.fromisoformat(start_date_str).timestamp())
        end_date = int(datetime.fromisoformat(end_date_str).timestamp())
        
        #Get weather data from function
        weather_data = get_historical_weather_data(lat, lon, start_date, end_date, API_KEY)
        
        #If it is fetched, return positive response
        if weather_data:
            logger.info(f"Retrieved historical weather data for location: {location}")
            return Response(weather_data)
        
        #If not, raise error
        else:
            logger.error(f"Failed to retrieve weather data for location: {location}")
            return JsonResponse({'error': 'Failed to retrieve weather data'})
