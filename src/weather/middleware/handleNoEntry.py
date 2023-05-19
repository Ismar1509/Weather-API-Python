from rest_framework.response import Response

#Error that can be raised if no entry is given
def handle_no_entry(message):
    return Response({'error': {message}})