from ..middleware.loggingMechanism import logger
from django.http import HttpResponse, JsonResponse
import base64
from django.contrib.auth import authenticate

def authentication (request):

    #Check if Authorization is in request header
    if 'Authorization' not in request.headers:

        #If it is not, create Unauthorized response
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="API"'
        return response
        
    # Extract and decode the Authorization header
    auth_header = request.headers['Authorization']

    #If header does not start with keyword Basic, create Unauthorized response
    if not auth_header.startswith('Basic '):
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="API"'
        return response

    #Split credentials and check second part, decode it and assign first part to username, second to password
    encoded_credentials = auth_header.split(' ')[1]
    credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username, password = credentials.split(':')

    # Log or print the username and password
    logger.info(f"Username: {username}")
    logger.info(f"Password: {password}")


    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    #If there is no user create unauthorized response
    if user is None:
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="API"'
        return response

#To enter the data, you need to fill authorization header
#
#You will need to create superuser with command py manage.py createsuperuser
#You should enter username, email, and password you want
#
#After that convert your usernam and password into base64 using online Basic Authentication Header Generator
#https://mixedanalytics.com/tools/basic-authentication-generator/
#
#Each time you want to fetch data using swagger and GET or POST request you will need to fill authorization header
#Fill it like this:
#
#Basic <base64username:password>
#e.g. your username is admin123 and password is softeng123
#
#Basic YWRtaW4xMjM6c29mdGVuZzEyMw==
#
#By using anything differently through swagger, you will not be able to fetch data

