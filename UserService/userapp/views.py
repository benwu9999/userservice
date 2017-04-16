from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world! This is our User App.")

from rest_framework import generics 
from userapp.models import User
from userapp.serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
