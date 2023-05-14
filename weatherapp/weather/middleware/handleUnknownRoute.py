from django.http import JsonResponse

def handle_unknown_route(request, path):
    return JsonResponse({'error': 'Page not found.'}, status=404)