from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'profileId', views.ProfileIdViewSet)
router.register(r'providerProfileId', views.ProviderProfileIdViewSet)
router.register(r'applicationId', views.ApplicationIdViewSet)
router.register(r'locationId', views.LocationIdViewSet)
router.register(r'jobPostId', views.JobPostIdViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^user/$', views.UserList.as_view()),
    # url(r'^user/(?P<userId>.+)$', views.UserDetail.as_view()),

    # endpoints for JWT token
    url(r'^admin/', admin.site.urls),
    url(r'^login/', obtain_jwt_token),
    url(r'^verify/', verify_jwt_token),
    url(r'^refresh/', refresh_jwt_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
