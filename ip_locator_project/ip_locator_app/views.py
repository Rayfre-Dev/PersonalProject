from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, IPAddressLocation
from .serializers import UserSerializer, IPAddressLocationSerializer
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class IPAddressLocationViewSet(viewsets.ModelViewSet):
    queryset = IPAddressLocation.objects.all()
    serializer_class = IPAddressLocationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ip_address = request.data.get('ip_address')
        user = request.user

        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch location data from IPbase API
        ipbase_response = requests.get(f'https://api.ipbase.com/v2/info?ip={ip_address}&apikey=ipb_live_GvBhYDH1Ji0lwNu4ia8gpDzgEAYCJOmp9H9p8bQI')
        ipbase_data = ipbase_response.json()
        
        # Print the full API response for debugging
        print(f"IPbase API response: {ipbase_data}")

        # Access the city name safely
        city = 'Unknown'
        location_data = ipbase_data.get('data', {}).get('location', {})
        if 'city' in location_data and 'name' in location_data['city']:
            city = location_data['city']['name']
        elif 'country' in location_data and 'name' in location_data['country']:
            city = location_data['country']['name']

        # Fetch population data from Data USA API
        datausa_response = requests.get(f'https://datausa.io/api/data?drilldowns=Place&measures=Population&year=latest')
        datausa_data = datausa_response.json()
        
        # Access the population safely
        population = datausa_data.get('data', [{}])[0].get('Population', 'Unknown')

        # Save the IP location
        ip_location = IPAddressLocation(user=user, ip_address=ip_address, location=city, population=population)
        ip_location.save()
        serializer = self.get_serializer(ip_location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
