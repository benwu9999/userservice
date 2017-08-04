# Create your views here.
import logging

from django.http import HttpResponse

from serializers import ProfileSerializer, SkillSerializer, CompensationSerializer, SkillIdSerializer


def index(request):
    return HttpResponse("Profile API")


from rest_framework import generics, status
from models import Profile, Compensation, Skill, SkillId
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


# uncomment the line below if you want to enable csrf protection for this view
# @method_decorator(csrf_protect, name='post')
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):

        request.data.pop('active', None)

        compensation = request.data.pop('compensation')
        comp, created = Compensation.objects.get_or_create(**compensation);
        request.data['compensation'] = comp

        skills = request.data.pop('skills')

        profile = Profile(**request.data)
        profile.save()
            # create skills and mapping
        for skill in skills:
            skill_data = {
                'skill': skill,
                'profile': profile.pk
            }
            skill, created = Skill.objects.get_or_create(**skill_data);
            skill_mapping = {
                'profile': profile.pk,
                'skill': skill.pk
            }
            skill_d, created = SkillId.objects.get_or_create(**skill_mapping);

        return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'profile_id'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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
