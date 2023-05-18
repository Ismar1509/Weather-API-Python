from datetime import datetime
import pytz


def responseBodyCurrent(data):
    weather_data = {
            'timestamp': data['dt'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'last_refresh_datetime': datetime.now(pytz.utc).astimezone(pytz.timezone('Europe/Sarajevo')).strftime("%Y-%m-%d %H:%M:%S")
        }
    return weather_data

def responseBodyForecast(data):
    weather_data = []
    for hour in data['list']:
            weather = {
                'timestamp': hour['dt'],
                'temperature': hour['main']['temp'],
                'humidity': hour['main']['humidity'],
                'wind_speed': hour['wind']['speed'],
                'description': hour['weather'][0]['description']
            }
            weather_data.append(weather)

    return weather_data  

def responseBodyHistorical(data):
    weather_data = []
    for hour in data['list']:
            weather = {
                'timestamp': hour['dt'],
                'temperature': hour['main']['temp'],
                'humidity': hour['main']['humidity'],
                'wind_speed': hour['wind']['speed'],
                'description': hour['weather'][0]['description']
            }
            weather_data.append(weather)

    return weather_data        
