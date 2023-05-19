from django.http import JsonResponse

#Error that is raised if wrong syntax is used
#e.g. localhost:8000/weather/
def handle_only_weather(request):
    return JsonResponse({'error': 'Wrong syntax.'}, status=404)