import geocoder
from geopy.distance import geodesic
from django.http import JsonResponse
from django.shortcuts import render

# The allowed location and radius in km
ALLOWED_LOCATION = (29.336821, 47.6751716)
#29.343868,48.0445074
RADIUS_KM = 10

class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user's IP address
        user_ip = self.get_user_ip(request)
        print(user_ip)
        if user_ip == "94.129.87.47":  # localhost
            user_location = 29.338, 47.675
        else:
             # Get the user's location based on their IP address
            user_location = self.get_location_from_ip(user_ip)

        # If the location is within the allowed range, let the request proceed
        if self.is_within_allowed_location(user_location):
            print(self.get_response(request))
            return self.get_response(request)
        else:
            # If the location is not within the allowed range, show an error page
            return render(request, 'home/error_page.html', {'message': 'You can only access this application from a specific location.'})

    def get_user_ip(self, request):
        """
        Extracts the real user IP address from the request headers if the app is behind a proxy.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        print(x_forwarded_for)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_from_ip(self, ip):
        """
        This function gets the latitude and longitude from the user's IP address.
        You can use a service like `geocoder` or other IP-based geolocation APIs.
        """
        try:
            g = geocoder.ip(ip)
            if g.ok:
                return g.latlng  # Returns a tuple of (latitude, longitude)
            else:
                return None
        except Exception as e:
            # Log or handle the exception if geocoding fails
            print(f"Error fetching geolocation for IP {ip}: {e}")
            return None

    def is_within_allowed_location(self, user_location):
        """
        Checks if the user's location is within the allowed radius.
        """
        if user_location:
            distance = geodesic(ALLOWED_LOCATION, user_location).kilometers
            print(f"User distance from allowed location: {distance} km")
            return distance <= RADIUS_KM
        return False
