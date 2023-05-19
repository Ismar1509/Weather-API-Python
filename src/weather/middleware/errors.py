from django.http import JsonResponse
from rest_framework.response import Response

def bad_request_error(message):
    return Response({'error': message}, status=400)

def not_found_error():
    return {'error':'City not found'}

def retrieve_location_error():
    return Response({'error': 'Failed to retrieve location'})

def server_error(message):
    return JsonResponse({'error': message}, status=500)