from django.contrib.auth.models import AnonymousUser

from apps.authentication.models import UserProfile
from apps.location.models import Location

def user_role(request):
    # Check if the user is authenticated
    locations= Location.objects.all()
    if isinstance(request.user, AnonymousUser):
        return {'user_role': None}  # For unauthenticated users
    
    try:
        # Fetch user role from the UserProfile model
        role = UserProfile.objects.get(user=request.user).role
    except UserProfile.DoesNotExist:
        role = None  # Handle case where user has no UserProfile
    
    return {'user_role': role,'locations':locations}
