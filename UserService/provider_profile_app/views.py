# Create your views here.
import logging
from datetime import datetime

import sys
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from models import ProviderProfile, BenefitId, Benefit
from serializers import ProviderProfileSerializer


def index(request):
    return HttpResponse("Profile API")


logger = logging.getLogger(__name__)


# uncomment the line below if you want to enable csrf protection for this view
# @method_decorator(csrf_protect, name='post')
class ProviderProfileList(generics.ListCreateAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer

    def post(self, request, *args, **kwargs):

        request.data.pop('active', None)
        benefits = request.data.pop('benefits')

        profile_dict = request.data
        if 'profile_id' not in profile_dict:
            profile_dict['created'] = datetime.utcnow()
            okStatus = status.HTTP_201_CREATED
        else:
            okStatus = status.HTTP_200_OK
        profile = ProviderProfile(**profile_dict)
        profile.save()

        # create benefits and mapping
        for benefit in benefits:
            benefit_data = {
                'benefit': benefit,
            }
            benefit, created = Benefit.objects.get_or_create(**benefit_data)
            benefit_mapping = {
                'profile': profile,
                'benefit': benefit
            }
            mapping, created = BenefitId.objects.get_or_create(**benefit_mapping);

        return Response(ProviderProfileSerializer(profile).data, status=okStatus)


class ProviderProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
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
        profiles = ProviderProfile.objects.filter(profile_id__in=request.data['ids'].split(','))
        return Response(profiles)


class ProviderProfileSearch(APIView):
    def get(self, request, format=None):
        try:
            if 'ids' in request.query_params:
                # data['locations'] = LocationSerializer(Location.objects.filter(
                #     pk__in=request.query_params['ids'].split(',')), many=True)

                serializer = ProviderProfileSerializer(ProviderProfile.objects.filter(
                    pk__in=request.query_params['ids'].split(',')), many=True)

                return Response(serializer.data)
        except:
            return Response(sys.exc_info()[0])
