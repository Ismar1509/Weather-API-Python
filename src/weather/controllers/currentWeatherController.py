from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from ..middleware.loggingMechanism import logger
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.currentWeatherRequestBody import current_weather_get_swagger, current_weather_post_swagger
from weather.controllers.getViews import getCurrentWeatherView
from weather.controllers.postViews import postCurrentWeatherView

#Decorators for request bodies (GET and POST) with swagger included
@current_weather_get_swagger
@current_weather_post_swagger

#Decorator that enables GET and POST methods to be performed
@api_view(['GET', 'POST'])

#Decorators that enable Basic Authentication and require user to be authenticated
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])

#Function to check which method is used and perform actions related to each method
def current_weather(request):
    if request.method == 'GET':
        return getCurrentWeatherView(request)
    
    elif request.method == 'POST':
        return Response(postCurrentWeatherView(request))
    
    else:
        logger.error(f"Invalid request method: {request.method}")
        return ('Invalid request method')