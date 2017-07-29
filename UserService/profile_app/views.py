# Create your views here.
import logging

from django.http import HttpResponse

from serializers import ProfileSerializer


def index(request):
    return HttpResponse("Profile API")


from rest_framework import generics
from models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# uncomment the line below if you want to enable csrf protection for this view
#@method_decorator(csrf_protect, name='post')
# class ProfileList(generics.ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#
#     # override the default lookup field "PK" with the lookup field for this model
#     lookup_field = 'profile_id'
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

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
