from django.http import JsonResponse

def handle_no_entry(request):
    return JsonResponse({'error': 'No location entered.'}, status=404)