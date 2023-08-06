# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .viewsets import OAuthApplicationViewset, AppResourcePermissionViewset, RequestHandshakeViewSet

router = DefaultRouter()

router.register(r'applications', OAuthApplicationViewset, base_name="oauth_application_list")
router.register(r'application_permissions', AppResourcePermissionViewset, base_name="oauth_application_permission_list")
router.register(r'handshake', RequestHandshakeViewSet, base_name="handshake_list")

urlpatterns = [
    url(r'^', include(router.urls)),
]
