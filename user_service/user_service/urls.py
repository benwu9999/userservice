from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<userId>[0-9a-f-]+)$', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
