from django.http import JsonResponse

def bad_request_error(message):
    return JsonResponse({'error': message}, status=400)

def not_found_error():
    return {'error':'City not found'}

def retrieve_location_error():
    return JsonResponse({'error': 'Failed to retrieve location'})

def server_error(message):
    return JsonResponse({'error': message}, status=500)