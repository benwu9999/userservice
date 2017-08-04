import logging
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets

from django.shortcuts import get_object_or_404, get_list_or_404

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("user service api")


class UserCreation(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        role_names = request.data.pop('roles')
        user = UserSerializer(data=request.data)
        # super(UserCreation, self).post(request, *args, **kwargs)
        if user.is_valid():
            saved_user = user.save()
            for role_name in role_names:
                role_data = {
                    'role': role_name,
                    'user': saved_user.pk
                }
                role = RoleSerializer(data=role_data)
                if role.is_valid():
                    role.save()
                else:
                    return Response(role.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserList(generics.ListAPIView):
#     # TODO should be set to authenticated in production for superuser only
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    # TODO should be set to authenticated in production for superuser only
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        resp = super(UserDetail, self).retrieve(request, *args, **kwargs)

        fltr = {'user_id': resp.data['user_id']}

        resp.data['roles'] = Role.objects.filter(**fltr).values_list('role', flat=True)

        resp.data['profile_ids'] = ProfileId.objects.filter(**fltr).values_list('profile_id', flat=True).order_by(
            'updated')

        resp.data['location_ids'] = LocationId.objects.filter(**fltr).values_list('location_id', flat=True).order_by(
            'updated')

        return resp


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        filter = {}
        filter['id'] = self.request.query_params['id']
        user = super(UserViewSet, self).get_object_or_404(queryset, **filter)
        d = {}
        if user:
            if user.role == 'SEEKER':
                d['applicationIds'] = user.application_id_set.all()
                d['locationIds'] = user.location_id_set.all()
                d['profileIds'] = user.profile_id_set.all()
            elif user.role == 'PROVIDER':
                d['jobPostIds'] = user.job_post_id_set.all()
                d['providerProfileIds'] = user.provider_profile_id_set.all()
            d['user'] = user
        return d

        #     def get_object(self):
        #         queryset = self.get_queryset()
        #         filter = {id=self.request.query_params['id']}
        #         user = get_object_or_404(queryset, **filter)
        #         d = {}
        #         d['applicationIds'] = user.application_id_set.all()
        #         d['locationIds'] = user.location_id_set.all()
        #         d['applicationIds'] = user.application_id_set.all()
        #         d['user'] = user
        #         return d

        # b.entry_set.all()


class ProfileIdCreation(generics.CreateAPIView):
    queryset = ProfileId.objects.all()
    serializer_class = ProfileIdSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('user_id')
        # queryset = User.objects.all()
        # filter = {'user_id': user_id}
        user = get_object_or_404(User, pk=user_id)

        data = {
            'profile_id': request.data['profile_id'],
            'user': user
        }
        profile_id_slz = ProfileIdSerializer(data=data)
        if profile_id_slz.is_valid():
            profile_id_slz.save()
        else:
            return Response(profile_id_slz.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(profile_id_slz.data, status=status.HTTP_201_CREATED)


class ApplicationIdCreation(generics.CreateAPIView):
    queryset = ApplicationId.objects.all()
    serializer_class = ApplicationIdSerializer

class LocationIdCreation(generics.CreateAPIView):
    queryset = LocationId.objects.all()
    serializer_class = LocationIdSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('user_id')
        # queryset = User.objects.all()
        # filter = {'user_id': user_id}
        user = get_object_or_404(User, pk=user_id)

        data = {
            'location_id': request.data['location_id'],
            'user': user
        }
        location = LocationIdSerializer(data=data)
        if location.is_valid():
            location.save()
        else:
            return Response(location.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(location.data, status=status.HTTP_201_CREATED)


class JobPostIdCreation(generics.CreateAPIView):
    queryset = JobPostId.objects.all()
    serializer_class = JobPostIdSerializer


class ProviderProfileIdCreation(generics.CreateAPIView):
    queryset = ProviderProfileId.objects.all()
    serializer_class = ProviderProfileIdSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('user_id')
        # queryset = User.objects.all()
        # filter = {'user_id': user_id}
        user = get_object_or_404(User, pk=user_id)

        data = {
            'profile_provider_id': request.data['profile_provider_id'],
            'user': user
        }
        provider_profile = ProviderProfileIdSerializer(data=data)
        if provider_profile.is_valid():
            provider_profile.save()
        else:
            return Response(provider_profile.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(provider_profile.data, status=status.HTTP_201_CREATED)