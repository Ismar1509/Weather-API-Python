from rest_framework import serializers

class CurrentWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=255)

class ForecastWeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(required=True, max_length=100)
    #days = serializers.IntegerField(required=False, min_value=1, max_value=7)
