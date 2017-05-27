"""ProfileService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),

    # need the '/' before $ to properly route call to generics.ListCreateAPIView
    url(r'^profile/$', views.ProfileList.as_view()),

    # supports /profile/{profileId}
    url(r'^profile/(?P<profileId>.+)$', views.ProfileDetail.as_view()),

    url(r'^profile/allIds$',views.AllIdsList.as_view()),
    url(r'^profile/ids=$',views.ProfileById.as_view()),
    url(r'^admin/', admin.site.urls),
]
