from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpRequest, JsonResponse
from weatherapp.serializers import HistoryWeatherRequestSerializer
from rest_framework.response import Response
import requests
import datetime


API_KEY = ''

def get_weather_history(location, start_date, end_date):
    start_timestamp = int(datetime.datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    
    api_url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={location[0]}&lon={location[1]}&start={start_timestamp}&end={end_timestamp}&appid={API_KEY}&units=metric'
    
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = f'Error {response.status_code}: {response.json()["message"]}'
        raise Exception(error_message)

@api_view(['GET', 'POST'])
def weather_history(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        if not location:
            return JsonResponse({'error': 'Location is required'}, status=400)
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        if not start_date:
            return JsonResponse({'error': 'Start date is required'}, status=400)
        if not end_date:
            return JsonResponse({'error': 'End date is required'}, status=400)
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        weather_data = get_weather_history(location, start_date, end_date)
        return JsonResponse(weather_data, safe=False)
    
    elif request.method == 'POST':
        serializer = HistoryWeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            # Get weather data for the location and dates
            weather_data = get_weather_history(location, start_date, end_date)
            # Return the weather data as a JSON response
            return Response(weather_data)
        else:
            # Return a bad request response if the serializer is not valid
            return Response(serializer.errors, status=400)
