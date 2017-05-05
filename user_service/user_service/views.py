import logging
from django.http import HttpResponse
from rest_framework import generics 
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello world! This is our User App.")


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'userId'
    queryset = User.objects.all()
    serializer_class = UserSerializer
