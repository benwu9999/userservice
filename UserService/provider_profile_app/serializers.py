from rest_framework import serializers
from models import ProviderProfile

class ProviderProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to conver Profile object data to primitive Python Data types
    """
    class Meta:
        model = ProviderProfile
        fields = '__all__'