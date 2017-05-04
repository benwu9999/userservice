from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to convert User object data to primitive Python datatypes
    """
    locationIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
                                        max_length=None)
    profileIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
                                       max_length=None)
    applicationIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
                                           max_length=None)
    roles = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
                                  max_length=None)


    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'userId', 'password', 'email', 'phone',
                  'profileIds', 'activeProfileId', 'locationIds', 'activeLocationId',
                  'applicationIds', 'roles', 'active', 'dateJoined')

    def create(self, validated_data):
        User.objects.create_user(**validated_data)
        return validated_data

    # Comma Separated String to List
    def string_to_list(self, data):
        if not isinstance(data, list):
            if data:
                data = [i for i in data.split(',')]
            else:
                data = []
        return data

    # List to Comma Separated String
    def list_to_string(self, data):
        if data:
            data = sorted(set(data))
            data = ','.join(str(i) for i in data)
        else:
            data = None
        return data

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['locationIds'] = self.string_to_list(instance['locationIds'])
            instance['profileIds'] = self.string_to_list(instance['profileIds'])
            instance['applicationIds'] = self.string_to_list(instance['applicationIds'])
            instance['roles'] = self.string_to_list(instance['roles'])
        else:
            instance.locationIds = self.string_to_list(instance.locationIds)
            instance.profileIds = self.string_to_list(instance.profileIds)
            instance.applicationIds = self.string_to_list(instance.applicationIds)
            instance.roles = self.string_to_list(instance.roles)
        return super(UserSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        ret = super(UserSerializer, self).to_internal_value(data)
        ret['locationIds'] = self.list_to_string(ret['locationIds'])
        ret['profileIds'] = self.list_to_string(ret['profileIds'])
        ret['applicationIds'] = self.list_to_string(ret['applicationIds'])
        ret['roles'] = self.list_to_string(ret['roles'])
        return ret
