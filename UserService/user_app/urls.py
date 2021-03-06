from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'user/user$', views.UserViewSet)
# router.register(r'user/profileId', views.ProfileIdViewSet)
# router.register(r'user/providerProfileId', views.ProviderProfileIdViewSet)
# router.register(r'user/applicationId', views.ApplicationIdViewSet)
# router.register(r'user/locationId', views.LocationIdViewSet)
# router.register(r'user/jobPostId', views.JobPostIdViewSet)

urlpatterns = [
    url(r'^user/admin', admin.site.urls),
    url(r'^$', views.index, name='index'),

    # url(r'^user/activate$', views.ActivateUser.as_view()),
    # url(r'^user/activateProfile$', views.UserCreation.as_view()),
    # url(r'^user/activateLocation', views.UserCreation.as_view()),
    # url(r'^user/addLocation', views.UserCreation.as_view()),
    url(r'^user/rel/addJobPost$', views.JobPostIdCreation.as_view()),
    url(r'^user/rel/deleteJobPost', views.DeleteJobPost.as_view()),

    url(r'^user/rel/addApplication$', views.ApplicationIdCreation.as_view()),
    url(r'^user/rel/deleteApplication', views.DeleteApplication.as_view()),

    url(r'^user/rel/addLocation$', views.LocationIdCreation.as_view()),
    url(r'^user/rel/deleteLocation', views.DeleteLocation.as_view()),
    url(r'^user/rel/activateLocation', views.ActivateLocation.as_view()),

    url(r'^user/rel/addProfile$', views.ProfileIdCreation.as_view()),
    url(r'^user/rel/deleteProfile', views.DeleteProfile.as_view()),
    url(r'^user/rel/activateProfile', views.ActivateProfile.as_view()),

    url(r'^user/rel/addProviderProfile$', views.ProviderProfileIdCreation.as_view()),
    url(r'^user/rel/deleteProviderProfile', views.DeleteProviderProfile.as_view()),

    url(r'^user/rel/addApplication$', views.ApplicationIdCreation.as_view()),

    url(r'^user/rel/addAlert$', views.JobPostAlertIdCreation.as_view()),
    url(r'^user/rel/alert$', views.JobPostAlertMapping.as_view()),
    url(r'^user/rel/deleteAlert', views.DeleteJobPostAlert.as_view()),

    url(r'^user$', views.UserCreation.as_view()),
    url(r'^user/exists/(?P<email>.+)$', views.UserExists.as_view()),
    url(r'^user/savePassword$', views.SavePassword.as_view()),
    # url(r'^user$', views.UserList.as_view()),
    url(r'^user/(?P<email>.+)$', views.UserDetail.as_view()),


    # endpoints for JWT token
    # url(r'^authService/login$', obtain_jwt_token),
    url(r'^authService/login$', obtain_jwt_token),
    url(r'^authService/verify$', verify_jwt_token),
    url(r'^authService/refresh$', refresh_jwt_token),

    url(r'^authService/resetPassword$', views.ResetPassword.as_view()),
    url(r'^authService/verifyResetId', views.VerifyResetId.as_view()),

]

# urlpatterns = router.urls

urlpatterns = format_suffix_patterns(urlpatterns)
