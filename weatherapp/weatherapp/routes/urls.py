"""
URL configuration for weatherapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from weather.controllers import handleOnlyWeather, handleNoEntry, currentWeatherController, historyWeatherController, forecastWeatherController, handleUnknownRoute


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('weather/current/', currentWeatherController.current_weather, name='current_weather'),
    path('weather/current/<str:path>', handleUnknownRoute.handle_unknown_route),

    path('weather/forecast/', forecastWeatherController.weather_forecast, name='weather_forecast'),
    path('weather/forecast/<str:path>', handleUnknownRoute.handle_unknown_route),

    path('weather/history/', historyWeatherController.historical_weather, name='weather_history'),
    path('weather/history/<str:path>', handleUnknownRoute.handle_unknown_route),
    
    path('<str:path>', handleUnknownRoute.handle_unknown_route),
    path('weather/', handleOnlyWeather.handle_only_weather)
]
