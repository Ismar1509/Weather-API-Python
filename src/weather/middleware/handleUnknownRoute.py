from django.http import JsonResponse

#Error that will be raised if requested page is not found
def handle_unknown_route(request, path):
    return JsonResponse({'error': 'Page not found.'}, status=404)