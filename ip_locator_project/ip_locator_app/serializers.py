from rest_framework import serializers
from .models import User, IPAddressLocation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'ip_address']

class IPAddressLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAddressLocation
        fields = '__all__'
