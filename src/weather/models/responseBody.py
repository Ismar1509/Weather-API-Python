#Response bodies for current, forecast and historical data
#Return list of important parameters - timestamp, temeperature, humidity, wind speed and description
#Time of last caching appends these responses in another function in views - weatherApi.py
def responseBodyCurrent(data):
    weather_data = {
            'timestamp': data['dt'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
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
