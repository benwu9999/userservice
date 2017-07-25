import logging
from django.http import HttpResponse
from rest_framework import generics, status

from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets



logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("user service api")


class UserCreation(generics.CreateAPIView):
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
                    'role' : role_name,
                    'user' : saved_user
                }
                role = RoleSerializer(data=role_data)
                if role.is_valid():
                    role.save()
                else:
                    return Response(role.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(generics.ListAPIView):
    # TODO should be set to authenticated in production for superuser only
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'user_id'
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

class ProfileIdViewSet(viewsets.ModelViewSet):
    queryset = ProfileId.objects.all()
    serializer_class = ProfileIdSerializer
    model = ProfileId

class ApplicationIdViewSet(viewsets.ModelViewSet):
    queryset = ApplicationId.objects.all()
    serializer_class = ApplicationIdSerializer
    model = ApplicationId

class LocationIdViewSet(viewsets.ModelViewSet):
    queryset = LocationId.objects.all()
    serializer_class = LocationIdSerializer
    model = LocationId

class JobPostIdViewSet(viewsets.ModelViewSet):
    queryset = JobPostId.objects.all()
    serializer_class = JobPostIdSerializer
    model = JobPostId

class ProviderProfileIdViewSet(viewsets.ModelViewSet):
    queryset = ProviderProfileId.objects.all()
    serializer_class = ProviderProfileIdSerializer
    model = ProviderProfileId
