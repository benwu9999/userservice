import logging
import operator
from datetime import datetime

import requests
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import *

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("user service api")


class UserExists(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ()
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs['email'])
        found = user.exists()
        ret = {
            'found': found
        }
        return JsonResponse(ret)


class SavePassword(generics.ListCreateAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            reset_id = data.pop('id')
            ele = reset_id.split('.')
            encoded_user_id = ele[0]
            token = ele[1]
            uid = urlsafe_base64_decode(encoded_user_id)
            existing_user = User.objects.get(pk=uid)
            if existing_user is not None and default_token_generator.check_token(existing_user, token):
                existing_user.set_password(data['password'])
                existing_user.save();
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)


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
            email = data['email']
            existing_user = User.objects.filter(pk=email)
            new_password = data.pop('new_password')
            user = User(**data)
            if not existing_user:
                okStatus = status.HTTP_201_CREATED
                user.set_password(data['password'])
            else:
                if new_password:
                    user.set_password(new_password)
                okStatus = status.HTTP_200_OK
            user.is_active = True
            user.save()
            # super(UserCreation, self).post(request, *args, **kwargs)
            for role_name in role_names:
                role_data = {
                    'role': role_name,
                    'email': user.pk,
                    'created': datetime.datetime.now()
                }
                existing_role = Role.objects.filter(email=user.pk, role=role_name)
                if not existing_role:
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
    permission_classes = (IsAuthenticated,)
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        resp = super(UserDetail, self).retrieve(request, *args, **kwargs)
        fltr = {'email': resp.data['email']}

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
            email = request.data.pop('email')
            # queryset = User.objects.all()
            # filter = {'email': email}
            user = get_object_or_404(User, pk=email)

            data = {
                'profile_id': request.data['profile_id'],
                'email': user,
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

        email = request.data.pop('email')
        user = User.objects.get(pk=email)
        if user and user.active_profile_id == profile_id:
            user.active_profile_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class ApplicationIdCreation(generics.CreateAPIView):
    queryset = ApplicationId.objects.all()
    serializer_class = ApplicationIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.pop('email')
            user = get_object_or_404(User, pk=email)

            data = {
                'application_id': request.data['application_id'],
                'email': user,
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
            email = request.data.pop('email')
            user = get_object_or_404(User, pk=email)

            data = {
                'alert_id': request.data['alert_id'],
                'email': user,
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
        has_no_user = 'emails' not in request.data or request.data['emails'] is None
        has_no_alert = 'alert_ids' not in request.data or request.data['alert_ids'] is None

        qs = list()
        if not has_no_alert:
            alert_ids = request.data['alert_ids'].split(',')
            qs.append(Q(pk__in=alert_ids))
        if has_no_user:
            users = User.objects.all()
        else:
            emails = request.data['emails'].split(',')
            users = User.objects.filter(pk__in=emails)
            qs.append(Q(user__in=emails))
        if qs:
            alert_mappings = JobPostAlertId.objects.filter(reduce(operator.and_, qs))
        else:
            alert_mappings = JobPostAlertId.objects.all()
        job_post_alert_d = JobPostAlertIdSerializer(alert_mappings, many=True).data

        user_d = UserSerializer(users, many=True).data

        email_to_user_d = dict()
        for u in user_d:
            email_to_user_d[u['email']] = u
        email_to_alert_ids_d = dict()
        for d in job_post_alert_d:
            alert_id = d['alert_id']
            email = d['email']
            user = email_to_user_d[email]

            if email not in email_to_alert_ids_d:
                email_to_alert_ids_d[email] = ComplexJson(user=user, alert_ids=[alert_id]);
            else:
                email_to_alert_ids_d[email].alert_ids.append(alert_id)

        for key, value in email_to_alert_ids_d.iteritems():
            email_to_alert_ids_d[key] = value.__dict__
        return Response(email_to_alert_ids_d)


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
            email = request.data.pop('email')
            user_by_email = get_object_or_404(User, pk=email)

            data = {
                'location_id': request.data['location_id'],
                'email': user_by_email,
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

        email = request.data.pop('email')
        user = User.objects.get(pk=email)
        if user and user.active_location_id == location_id:
            user.active_location_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class JobPostIdCreation(generics.CreateAPIView):
    queryset = JobPostId.objects.all()
    serializer_class = JobPostIdSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.pop('email')
            user = get_object_or_404(User, pk=email)

            data = {
                'job_post_id': request.data['job_post_id'],
                'email': user,
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
            email = request.data.pop('email')
            user = get_object_or_404(User, pk=email)

            data = {
                'provider_profile_id': request.data['provider_profile_id'],
                'email': user,
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

        email = request.data.pop('email')
        user = User.objects.get(pk=email)
        if user and user.active_profile_id == provider_profile_id:
            user.active_profile_id = None;
            user.save();
        return Response(status=status.HTTP_200_OK)


class ActivateProfile(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.pop('email')
        user = get_object_or_404(User, pk=email)
        user.active_profile_id = request.data['profile_id']
        user.save();
        return Response(status=status.HTTP_200_OK)


class ActivateLocation(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.pop('email')
        user = get_object_or_404(User, pk=email)
        user.active_location_id = request.data['location_id']
        user.save();
        return Response(status=status.HTTP_200_OK)


from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class ResetPassword(generics.CreateAPIView):
    key = 'key-992449508ab9bedb746eb2b72af6e01f'
    sandbox = 'sandbox4ce17324a56c48e28aa83dcb313ed504.mailgun.org'

    permission_classes = ()

    # token_generator = OneseekPasswordResetTokenGenerator()

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.pop('email')
            existing_user = User.objects.get(pk=email)
            if existing_user:
                self._send_email(existing_user, email);
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)

    def _send_email(self, user, email):
        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox)
        template = loader.get_template('email_template.html')
        encoded_user_id = urlsafe_base64_encode(force_bytes(email))
        token = default_token_generator.make_token(user)
        context = {
            'reset_link': "http://localhost:4200/home/confirmResetPassword?id=" + encoded_user_id + '.' + token,
        }
        html = template.render(context)
        request = requests.post(
            request_url,
            auth=("api", self.key),
            data={
                "from": "hello@example.com",
                "to": email,
                "subject": "Oneseek Password Reset",
                "text": 'html version of email failed to display',
                "html": html,
            }
        )
        print('Status: {0}'.format(request.status_code))
        print('Body:   {0}'.format(request.text))


class VerifyResetId(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        reset_id = request.GET['id']
        ele = reset_id.split('.')
        encoded_user_id = ele[0]
        token = ele[1]
        uid = urlsafe_base64_decode(encoded_user_id)
        existing_user = User.objects.get(pk=uid)
        if existing_user is not None and default_token_generator.check_token(existing_user, token):
            return Response(uid, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ConfirmResetPassword(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ()
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs['email'])
        found = user.exists()
        ret = {
            'found': "true",
        }
        return Response(ret, status=status.HTTP_200_OK)


class Utils():
    @staticmethod
    def create_rel(clazz, request, idAttributeName, slz):
        email = request.data.pop('email')
        user = get_object_or_404(User, pk=email)

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
