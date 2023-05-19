from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User

class CustomFileBackend(BaseAuthentication):
    def authenticate(self, request):
        # Read the entered password from the request
        password = request.POST.get('password')

        # Read the stored password from a local file
        with open('weatherapp\password.txt', 'r') as f:
            stored_password = f.read().strip()

        # Compare the entered password with the stored password
        if password == stored_password:
            # Create or retrieve the user object
            user, _ = User.objects.get_or_create(username='user')
            return user

        return None