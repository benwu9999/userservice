# Create your views here.
import logging

from django.http import HttpResponse

from serializers import ProviderProfileSerializer


def index(request):
    return HttpResponse("Profile API")


from rest_framework import generics
from models import ProviderProfile
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# uncomment the line below if you want to enable csrf protection for this view
#@method_decorator(csrf_protect, name='post')
class ProviderProfileList(generics.ListCreateAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer


class ProviderProfileDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'profile_id'
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer


class AllIdsList(APIView):
    """
    Return a list of profileIds
    """

    def get(self, request, format=None):
        allIdList = sorted([x['profileId'] for x in ProviderProfile.objects.values('profileId')])
        return Response(data=allIdList)

class ProviderProfileById(APIView):

    def get(self, request, format=None):
        profiles = ProviderProfile.objects.filter(profile_id__in = request.data['ids'].split(','))
        return Response(profiles)
