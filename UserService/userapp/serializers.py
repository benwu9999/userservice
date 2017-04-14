from rest_framework import serializers
from userapp.models import User

class UserSerializer(serializers.ModelSerializer):
	"""
	Serializer to convert User object data to primitive Python datatypes
	"""

	class Meta:
		model=User
		fields=('firstName', 'lastName', 'userId', 'password', 'email', 'phone', 
			'profileIds', 'activeProfileId', 'locationIds', 'activeLocationId',
			'applicationIds', 'roles', 'active', 'date_joined')

	def create (self, validated_data):
		User.objects.create_user(**validated_data)
		return validated_data

