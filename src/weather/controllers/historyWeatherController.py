from ..controllers.postViews import postHistoryWeatherView
from ..controllers.getViews import getHistoryWeatherView
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..middleware.loggingMechanism import logger
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.historyWeatherRequestBody import history_weather_get_swagger, history_weather_post_swagger

#Decorators for request bodies (GET and POST) with swagger included
@history_weather_get_swagger
@history_weather_post_swagger

#Decorator to allow Django Cross-Site Request Forgery to be removed
#Multiple requests can be processed without requiring a valid CSRF token.
@csrf_exempt

#Decorator that enables GET and POST methods to be performed
@api_view(['GET', 'POST'])

#Decorators that enable Basic Authentication and require user to be authenticated
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])

#Function to check which method is used and perform actions related to each method
def historical_weather(request):
    if request.method == 'GET':
       return getHistoryWeatherView(request)
        
    elif request.method == 'POST':
        return postHistoryWeatherView(request)
        
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'})




