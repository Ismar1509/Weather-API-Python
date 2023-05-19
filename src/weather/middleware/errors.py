from django.http import JsonResponse
from rest_framework.response import Response

#Error that is raised when bad request is given
def bad_request_error(message):
    return Response({'error': message}, status=400)

#Error that can be raised when city is not found
def not_found_error():
    return {'error':'City not found'}

#Error that can be raised if fetching location is unsuccessful
def retrieve_location_error():
    return Response({'error': 'Failed to retrieve location'})

#Error that can be raised if server error occurs
def server_error(message):
    return JsonResponse({'error': message}, status=500)