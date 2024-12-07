from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from geopy.distance import geodesic
import geocoder

# Allowed location and radius in km
ALLOWED_LOCATION = (29.336821, 47.6751716)
#29.343868,48.0445074
RADIUS_KM = 10

class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = self.get_user_ip(request)

        # Simulate localhost location for development
        if user_ip == "127.0.0.1":  
            user_location = (29.338, 47.675)
        else:
            user_location = self.get_location_from_ip(user_ip)

        if not self.is_within_allowed_location(user_location):
            # Render error page and terminate further processing
            return render(request, 'home/error_page.html', {
                'message': 'You can only access this application from a specific location.'
            }, status=403)

        # Allow the request to proceed
        return self.get_response(request)

    def get_user_ip(self, request):
        """
        Extract the user's real IP address from request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_from_ip(self, ip):
        """
        Fetch latitude and longitude from IP address using geocoder.
        """
        try:
            g = geocoder.ip(ip)
            if g.ok:
                return g.latlng  # (latitude, longitude)
            else:
                return None
        except Exception as e:
            print(f"Error fetching geolocation for IP {ip}: {e}")
            return None

    def is_within_allowed_location(self, user_location):
        """
        Check if the user's location is within the allowed radius.
        """
        if user_location:
            distance = geodesic(ALLOWED_LOCATION, user_location).kilometers
            print(f"User distance from allowed location: {distance} km")
            return distance <= RADIUS_KM
        return False
