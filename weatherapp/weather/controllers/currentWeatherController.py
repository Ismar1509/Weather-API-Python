import base64
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from weatherapp.serializers import CurrentWeatherRequestSerializer
from ..middleware.errors import bad_request_error, not_found_error, server_error
from .weatherApi import get_weather_current_response
import requests
from ..middleware.loggingMechanism import logger
from .API_KEY import API_KEY
from .pswrd import PASSWORD
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



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
    operation_summary='Request current weather',
    operation_description='Request current weather for a specific location',
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
                description='The name of the location to get the weather for',
                example='Sarajevo'
            ),
        },
        required=['location']
    ),
    responses={
        200: 'A successful response',
        400: 'Bad request',
        401: 'Unauthorized',
        500: 'Internal server error',
    }
)




@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def current_weather(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        #password = request.data.get('password')
    	
        
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