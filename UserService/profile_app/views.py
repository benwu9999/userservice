# Create your views here.
import logging
from datetime import datetime

import sys
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from models import Profile, Compensation, Skill, SkillId
from serializers import ProfileSerializer


def index(request):
    return HttpResponse("Profile API")


logger = logging.getLogger(__name__)


# uncomment the line below if you want to enable csrf protection for this view
# @method_decorator(csrf_protect, name='post')
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):

        request.data.pop('active', None)
        skills = request.data.pop('skills')

        now = datetime.utcnow()

        compensation = request.data.pop('compensation')
        compensation['created'] = now
        comp, created = Compensation.objects.get_or_create(**compensation)

        profile_dict = request.data
        if 'profile_id' not in profile_dict:
            profile_dict['created'] = now
            okStatus = status.HTTP_201_CREATED
        else:
            okStatus = status.HTTP_200_OK
        profile = Profile(**profile_dict)
        profile.save()

        # create skills and mapping
        for skill in skills:
            skill_data = {
                'skill': skill,
                # 'profile': profile.pk
            }
            skill, created = Skill.objects.get_or_create(**skill_data)
            skill_mapping = {
                'profile': profile,
                'skill': skill
            }
            mapping, created = SkillId.objects.get_or_create(**skill_mapping);

        z = ProfileSerializer(profile)
        return Response(z.data, status=okStatus)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with
    # the lookup field for this model
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileSearch(APIView):
    def get(self, request, format=None):
        try:
            args = Q()
            kwargs = {}
            if 'ids' in request.query_params:
                kwargs['pk__in'] = request.query_params['ids'].split(',')
            if 'within' in request.query_params:
                kwargs['created__gt'] = get_epoch(request.query_params['within'])
            if 'has' in request.query_params:
                args = args | Q(**{'name__icontains':request.query_params['has']})
                args = args | Q(**{'description__icontains': request.query_params['has']})
                args = args | Q(**{'email__icontains': request.query_params['has']})
                args = args | Q(**{'phone__icontains': request.query_params['has']})
                args = args | Q(**{'other_contact__icontains': request.query_params['has']})
            z = ProfileSerializer(Profile.objects.filter(*args, **kwargs), many=True)
            return Response(z.data)
        except:
            return Response(sys.exc_info()[0])

# class AllIdsList(APIView):
#     """
#     Return a list of profileIds
#     """

#     def get(self, request, format=None):
#         allIdList = sorted([x['profileId'] for x in Profile.objects.values('profileId')])
#         return Response(data=allIdList)

# class ProfileById(APIView):
#
#     def get(self, request, format=None):
#         profiles = Profile.objects.filter(profile_id__in = request.data['ids'].split(','))
#         return Response(profiles)
