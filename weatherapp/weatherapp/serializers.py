from rest_framework import serializers

class CurrentWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=255)

class ForecastWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=100)
    days = serializers.IntegerField(required=True, min_value=1, max_value=7)

class HistoryWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, help_text='City name and country code, e.g. London,UK')
    start_date = serializers.DateField(required=True, help_text='Starting date in YYYY-MM-DD format')
    end_date = serializers.DateField(required=True, help_text='Ending date in YYYY-MM-DD format')

    

