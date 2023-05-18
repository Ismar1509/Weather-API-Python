import base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from weatherapp.serializers import CurrentWeatherRequestSerializer
from ..middleware.errors import bad_request_error
from .weatherApi import get_weather_current_response
from ..middleware.loggingMechanism import logger
from .API_KEY import API_KEY
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from ..swagger.currentWeatherSwagger import current_weather_get_swagger, current_weather_post_swagger

@current_weather_get_swagger
@current_weather_post_swagger
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
        return JsonResponse(weather_data)
    
    elif request.method == 'POST':
        serializer = CurrentWeatherRequestSerializer(data=request.data)

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
    else:
        logger.error(f"Invalid request method: {request.method}")