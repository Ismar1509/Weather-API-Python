from rest_framework import serializers
from django.contrib.auth.models import User

#Serializes and validates the request data for fetching current weather.
class CurrentWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=255)

#Serializes and validates the request data for fetching weather forecast.
class ForecastWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=100)
    days = serializers.IntegerField(required=True, min_value=1, max_value=7)

#Serializes and validates the request data for fetching historical weather.
class HistoryWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, help_text='City name and country code, e.g. London,UK')
    start_date = serializers.DateField(required=True, help_text='Starting date in YYYY-MM-DD format')
    end_date = serializers.DateField(required=True, help_text='Ending date in YYYY-MM-DD format')

#Serializes the User model data.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    

#Serializers are used to convert complex data types, such as models or dictionaries, into JSON-serializable representations. 
#They also handle validation of incoming data based on field definitions, ensuring that the data is in the expected format before further processing.