# Create your views here.
import logging
import operator
import sys

from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from models import ProviderProfile, BenefitId, Benefit
from serializers import ProviderProfileSerializer
from shared.utils import Utils


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
    permission_classes = ()

    def get(self, request, format=None):
        try:
            qs = list()
            if 'ids' in request.query_params:
                qs.append(Q(pk__in=request.query_params['ids'].split(',')))
            if 'within' in request.query_params:
                qs.append(Q(created__gt=Utils.get_epoch(request.query_params['within'])))
            if 'has' in request.query_params:
                for param in request.query_params['has'].split(","):
                    text_qs = list()
                    text_qs.append(Q(**{'company_name__icontains': param}))
                    text_qs.append(Q(**{'description__icontains': param}))
                    text_qs.append(Q(**{'email__icontains': param}))
                    text_qs.append(Q(**{'phone__icontains': param}))
                    text_qs.append(Q(**{'other_contact__icontains': param}))
                    qs.append(reduce(operator.or_, text_qs))
            z = ProviderProfileSerializer(ProviderProfile.objects.filter(reduce(operator.or_, qs)), many=True)
            # z = ProviderProfileSerializer(ProviderProfile.objects.filter(reduce(operator.and_, qs)), many=True)
            return Response(z.data)
        except:
            return Response(sys.exc_info()[0])


class ProviderProfileByText(GenericAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            id_only = False
            if 'id_only' in request.data and request.data['id_only'] == True:
                id_only = True

            # profile id -> profile dict
            id_dict = dict()
            # text -> [ids...]
            text_to_id_dict = dict()
            if 'has' in request.data:
                if id_only:
                    for param in request.data['has'].split(","):
                        text_qs = self.create_qs(param)
                        ids = ProviderProfile.objects.values_list('profile_id', flat=True).filter(
                            reduce(operator.or_, text_qs))
                        text_to_id_dict[param] = ids
                    return Response(text_to_id_dict)
                else:
                    for param in request.data['has'].split(","):
                        text_qs = self.create_qs(param)
                        z = ProviderProfileSerializer(ProviderProfile.objects.filter(reduce(operator.or_, text_qs)),
                                                      many=True)
                        ids = list()
                        for p in z.data:
                            id = p['profile_id']
                            if id not in id_dict:
                                id_dict[id] = p
                            ids.append(id)
                        text_to_id_dict[param] = ids
                    ret = dict()
                    ret['idDict'] = id_dict
                    ret['textDict'] = text_to_id_dict
                    return Response(ret)
        except:
            return Response(sys.exc_info()[0])

    def create_qs(self, param):
        text_qs = list()
        text_qs.append(Q(**{'company_name__icontains': param}))
        text_qs.append(Q(**{'description__icontains': param}))
        text_qs.append(Q(**{'email__icontains': param}))
        text_qs.append(Q(**{'phone__icontains': param}))
        text_qs.append(Q(**{'other_contact__icontains': param}))
        return text_qs


class ProviderProfileSearchByIds(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        if 'ids' in request.query_params:
            q = Q(pk__in=request.query_params['ids'].split(','))
            z = ProviderProfileSerializer(ProviderProfile.objects.filter(q), many=True)
            return Response(z.data)
        return Response([])
