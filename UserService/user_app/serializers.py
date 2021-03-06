from rest_framework import serializers
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to convert User object data to primitive Python datatypes
    """

    # commenting this out now for testing JWT authentication
    # locationIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
    #                                     max_length=None)
    # profileIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
    #                                    max_length=None)
    # applicationIds = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
    #                                        max_length=None)
    # roles = serializers.ListField(child=serializers.UUIDField(format='hex_verbose'), min_length=None,
    #                               max_length=None)

    class Meta:
        model = User
        fields = '__all__'

        # overwriting create method to call user.set_password, this call is needed to hash the password
        # which is by default the way django authenticate a login, django will try to unhash the hashed
        # password in database to authenticate user login
        # def create(self, validated_data):
        #     user = User.objects.create(user_id=validated_data['user_id'])
        #     user.set_password(validated_data['password'])
        #     user.is_active = True
        #     user.save()
        #     return user

        # user = super(UserSerializer, self).create(validated_data)
        # user.set_password(validated_data['password'])
        # user.is_active = True
        # user.save()
        # return user

        # force django to return userId only in response to POST call to create user
        # has to create a json object
        # def to_representation(self, user):
        #     return {
        #         'userId': user.user_id
        #     }
        #

        # # Comma Separated String to List
        # def string_to_list(self, data):
        #     if not isinstance(data, list):
        #         if data:
        #             data = [i for i in data.split(',')]
        #         else:
        #             data = []
        #     return data
        #
        # # List to Comma Separated String
        # def list_to_string(self, data):
        #     if data:
        #         data = sorted(set(data))
        #         data = ','.join(str(i) for i in data)
        #     else:
        #         data = None
        #     return data

        # def to_representation(self, instance):
        #     if isinstance(instance, dict):
        #         instance['locationIds'] = self.string_to_list(instance['locationIds'])
        #         instance['profileIds'] = self.string_to_list(instance['profileIds'])
        #         instance['applicationIds'] = self.string_to_list(instance['applicationIds'])
        #         instance['roles'] = self.string_to_list(instance['roles'])
        #     else:
        #         instance.locationIds = self.string_to_list(instance.locationIds)
        #         instance.profileIds = self.string_to_list(instance.profileIds)
        #         instance.applicationIds = self.string_to_list(instance.applicationIds)
        #         instance.roles = self.string_to_list(instance.roles)
        #     return super(UserSerializer, self).to_representation(instance)
        #
        # def to_internal_value(self, data):
        #     ret = super(UserSerializer, self).to_internal_value(data)
        #     ret['locationIds'] = self.list_to_string(ret['locationIds'])
        #     ret['profileIds'] = self.list_to_string(ret['profileIds'])
        #     ret['applicationIds'] = self.list_to_string(ret['applicationIds'])
        #     ret['roles'] = self.list_to_string(ret['roles'])
        #     return ret


class ProfileIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileId
        fields = '__all__'

    profile_id = serializers.UUIDField(format='hex')

    def create(self, validated_data):
        id, created = ProfileId.objects.get_or_create(**validated_data);
        return id;


class ProviderProfileIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfileId
        fields = '__all__'

    provider_profile_id = serializers.UUIDField(format='hex')

class LocationIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationId
        fields = '__all__'

    location_id = serializers.UUIDField(format='hex')

class JobPostIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostId
        fields = '__all__'

    job_post_id = serializers.UUIDField(format='hex')

class ApplicationIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationId
        fields = '__all__'

    application_id = serializers.UUIDField(format='hex')

class JobPostAlertIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostAlertId
        fields = '__all__'

    # alert_id = serializers.UUIDField(format='hex')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
