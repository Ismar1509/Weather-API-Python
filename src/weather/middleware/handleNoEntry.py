from rest_framework.response import Response

def handle_no_entry(message):
    return Response({'error': {message}})