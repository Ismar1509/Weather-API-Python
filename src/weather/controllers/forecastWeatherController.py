from ..controllers.postViews import postForecastWeatherView
from ..controllers.getViews import getForecastWeatherView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from ..middleware.loggingMechanism import logger
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.forecastWeatherRequestBody import forecast_weather_get_swagger, forecast_weather_post_swagger

#Decorators for request bodies (GET and POST) with swagger included
@forecast_weather_get_swagger
@forecast_weather_post_swagger

#Decorator that enables GET and POST methods to be performed
@api_view(['GET', 'POST'])

#Decorators that enable Basic Authentication and require user to be authenticated
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])

#Function to check which method is used and perform actions related to each method
def weather_forecast(request):
    if request.method == 'GET':
        return getForecastWeatherView(request)
    
    elif request.method == 'POST':
        return postForecastWeatherView(request)
    
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})

