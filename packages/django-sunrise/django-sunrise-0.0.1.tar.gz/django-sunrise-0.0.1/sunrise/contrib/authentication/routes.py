# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from .viewsets import CustomerViewSet, SunriseProfileViewSet, PageGroupViewSet, SunriseRoleViewSet, RolePageAccessViewSet, SunriseProfileRolesAssignedViewSet, UserViewset, SearchCriteria

router = DefaultRouter()

router.register(r'customer', CustomerViewSet, base_name="customer_list")
router.register(r'user', UserViewset, base_name="user_list")
router.register(r'sunrise_profile', SunriseProfileViewSet, base_name="sunrise_profile_list")
router.register(r'page_group', PageGroupViewSet, base_name="page_group_list")
router.register(r'sunrise_role', SunriseRoleViewSet, base_name="sunrise_role_list")
router.register(r'role_page_access', RolePageAccessViewSet, base_name="role_page_accessr_list")
router.register(r'sunrise_profile_roles_assigned', SunriseProfileRolesAssignedViewSet, base_name="sunrise_profile_roles_assigned_list")
router.register(r'search_criteria', SearchCriteria, base_name="search_criteria")

urlpatterns = [
    url(r'^', include(router.urls)),
]
