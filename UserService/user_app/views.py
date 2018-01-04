import logging
from collections import defaultdict

from datetime import datetime

import operator
from uuid import UUID

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from django.db.models.query_utils import Q
from .serializers import *
from rest_framework import viewsets

from django.shortcuts import get_object_or_404, get_list_or_404

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("user service api")


class UserCreation(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data.pop('locations')
            data.pop('profiles')
            data.pop('alerts')
            data.pop('applications')

            role_names = data.pop('roles')
            if 'user_id' not in data:
                okStatus = status.HTTP_201_CREATED
            else:
                okStatus = status.HTTP_200_OK
            user = User(**data)
            user.set_password(data['password'])
            user.is_active = True
            user.save()
            # super(UserCreation, self).post(request, *args, **kwargs)
            for role_name in role_names:
                role_data = {
                    'role': role_name,
                    'user': user.pk,
                    'created': datetime.datetime.now()
                }
                z = RoleSerializer(data=role_data)
                if z.is_valid():
                    z.save()
                else:
                    return Response(z.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(UserSerializer(user).data, status=okStatus)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)
        # else:
        #     return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if 'SEEKER' in resp.data['roles']:
            resp.data['profile_ids'] = ProfileId.objects.filter(**fltr).values_list('profile_id', flat=True).order_by(
                'created')
        else:
            resp.data['profile_ids'] = ProviderProfileId.objects.filter(**fltr). \
                values_list('provider_profile_id', flat=True).order_by(
                'created')

        resp.data['location_ids'] = LocationId.objects.filter(**fltr).values_list('location_id', flat=True).order_by(
            'created')

        resp.data['application_ids'] = ApplicationId.objects.filter(**fltr).values_list('application_id',
                                                                                        flat=True).order_by('created')

        resp.data['alert_ids'] = JobPostAlertId.objects.filter(**fltr).values_list('alert_id', flat=True).order_by(
            'created')

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
                d['alertIds'] = user.job_post_id_set.all()
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
        try:
            user_id = request.data.pop('user_id')
            # queryset = User.objects.all()
            # filter = {'user_id': user_id}
            user = get_object_or_404(User, pk=user_id)

            data = {
                'profile_id': request.data['profile_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            profile_id = ProfileId(**data)
            profile_id.save()
            return Response(ProfileIdSerializer(profile_id).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

class DeleteProfile(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        profile_id = request.data.pop('profile_id')
        profile_rel = ProfileId.objects.get(pk=profile_id)
        if profile_rel:
            profile_rel.delete()

        user_id = request.data.pop('user_id')
        user = User.objects.get(pk=user_id)
        if user and user.active_profile_id == profile_id:
            user.active_profile_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class ApplicationIdCreation(generics.CreateAPIView):
    queryset = ApplicationId.objects.all()
    serializer_class = ApplicationIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.pop('user_id')
            user = get_object_or_404(User, pk=user_id)

            data = {
                'application_id': request.data['application_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            application_id = ApplicationId(**data)
            application_id.save()
            return Response(ApplicationIdSerializer(application_id).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

class JobPostAlertIdCreation(generics.CreateAPIView):
    queryset = JobPostAlertId.objects.all()
    serializer_class = JobPostAlertIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.pop('user_id')
            user = get_object_or_404(User, pk=user_id)

            data = {
                'alert_id': request.data['alert_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            mapping = JobPostAlertId(**data)
            mapping.save()
            z = JobPostAlertIdSerializer(mapping)
            return Response(z.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

class JobPostAlertMapping(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = JobPostAlertId.objects.all()
    serializer_class = JobPostAlertIdSerializer

    def post(self, request, *args, **kwargs):
        has_no_user = 'user_ids' not in request.data or request.data['user_ids'] is None
        has_no_alert = 'alert_ids' not in request.data or request.data['alert_ids'] is None

        qs = list()
        if not has_no_alert:
            alert_ids = request.data['alert_ids'].split(',')
            qs.append(Q(pk__in=alert_ids))
        if has_no_user:
            users = User.objects.all()
        else:
            user_ids = request.data['user_ids'].split(',')
            users = User.objects.filter(pk__in=user_ids)
            qs.append(Q(user__in=user_ids))
        if qs:
            alert_mappings = JobPostAlertId.objects.filter(reduce(operator.and_, qs))
        else:
            alert_mappings = JobPostAlertId.objects.all()
        job_post_alert_d = JobPostAlertIdSerializer(alert_mappings, many=True).data

        user_d = UserSerializer(users, many=True).data

        user_id_to_user_d = dict()
        for u in user_d:
            user_id_to_user_d[u['user_id']] = u
        user_id_to_alert_ids_d = dict()
        for d in job_post_alert_d:
            alert_id = d['alert_id']
            user_id = d['user']
            user = user_id_to_user_d[user_id]

            if user_id not in user_id_to_alert_ids_d:
                user_id_to_alert_ids_d[user_id] = ComplexJson(user=user, alert_ids=[alert_id]);
            else:
                user_id_to_alert_ids_d[user_id].alert_ids.append(alert_id)

        for key, value in user_id_to_alert_ids_d.iteritems():
            user_id_to_alert_ids_d[key] = value.__dict__
        return Response(user_id_to_alert_ids_d)


class DeleteJobPostAlert(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        alert_id = request.data.pop('alert_id')
        job_post_alert_id = JobPostAlertId.objects.get(pk=alert_id)
        if job_post_alert_id:
            job_post_alert_id.delete()
        return Response(status=status.HTTP_200_OK)


class DeleteApplication(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        application_id = request.data.pop('application_id')
        application_rel = ApplicationId.objects.get(pk=application_id)
        if application_rel:
            application_rel.delete()
        return Response(status=status.HTTP_200_OK)


class LocationIdCreation(generics.CreateAPIView):
    queryset = LocationId.objects.all()
    serializer_class = LocationIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.pop('user_id')
            # queryset = User.objects.all()
            # filter = {'user_id': user_id}
            user = get_object_or_404(User, pk=user_id)

            data = {
                'location_id': request.data['location_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            location_id = LocationId(**data)
            location_id.save()
            return Response(LocationIdSerializer(location_id).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)


class DeleteLocation(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        location_id = request.data.pop('location_id')
        location_rel = LocationId.objects.get(pk=location_id)
        if location_rel:
            location_rel.delete()

        user_id = request.data.pop('user_id')
        user = User.objects.get(pk=user_id)
        if user and user.active_location_id == location_id:
            user.active_location_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class JobPostIdCreation(generics.CreateAPIView):
    queryset = JobPostId.objects.all()
    serializer_class = JobPostIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.pop('user_id')
            user = get_object_or_404(User, pk=user_id)

            data = {
                'job_post_id': request.data['job_post_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            job_post_id = JobPostId(**data)
            job_post_id.save()
            return Response(JobPostIdSerializer(job_post_id).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

class DeleteJobPost(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        job_post_id = request.data.pop('job_post_id')
        job_post_rel = JobPostId.objects.get(pk=job_post_id)
        if job_post_rel:
            job_post_rel.delete()
        return Response(status=status.HTTP_200_OK)


class ProviderProfileIdCreation(generics.CreateAPIView):
    queryset = ProviderProfileId.objects.all()
    serializer_class = ProviderProfileIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.pop('user_id')
            user = get_object_or_404(User, pk=user_id)

            data = {
                'provider_profile_id': request.data['provider_profile_id'],
                'user': user,
                'created': datetime.datetime.now()
            }
            profile_id = ProviderProfileId(**data)
            profile_id.save()
            return Response(ProviderProfileIdSerializer(profile_id).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

class DeleteProviderProfile(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        provider_profile_id = request.data.pop('provider_profile_id')
        provider_profile = ProviderProfileId.objects.get(pk=provider_profile_id)
        if provider_profile:
            provider_profile.delete()

        user_id = request.data.pop('user_id')
        user = User.objects.get(pk=user_id)
        if user and user.active_profile_id == provider_profile_id:
            user.active_profile_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class ActivateProfile(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('user_id')
        user = get_object_or_404(User, pk=user_id)
        user.active_profile_id = request.data['profile_id']
        user.save();
        return Response(status=status.HTTP_200_OK)


class ActivateLocation(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('user_id')
        user = get_object_or_404(User, pk=user_id)
        user.active_location_id = request.data['location_id']
        user.save();
        return Response(status=status.HTTP_200_OK)


class Utils():
    @staticmethod
    def createRel(clazz, request, idAttributeName, slz):
        user_id = request.data.pop('user_id')
        user = get_object_or_404(User, pk=user_id)

        data = {
            idAttributeName: request.data[idAttributeName],
            'user': user,
        }
        z = slz(data=data)
        if z.is_valid():
            z.save()
        else:
            return Response(z.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(z.data[idAttributeName], status=status.HTTP_201_CREATED)

    @staticmethod
    def deleteRel(clazz, request, idAttributeName):
        id = request.data.pop(idAttributeName)
        rel = clazz.objects.get(pk=id)
        if rel:
            rel.delete()
        return Response(status=status.HTTP_200_OK)


class ComplexJson(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
