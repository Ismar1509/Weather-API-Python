from django.http import JsonResponse

def handle_only_weather(request):
    return JsonResponse({'error': 'Wrong syntax.'}, status=404)