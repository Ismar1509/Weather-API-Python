from django.db import models
from django.http import HttpRequest

class RequestBody:
    def __init__(self, request: HttpRequest):
        self.city = request.POST.get('city', '')
        self.password = request.POST.get('password', '')
