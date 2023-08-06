# Author: Integra
# Dev: Partha (Ref)

from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .viewsets import MenuStructureViewset, AddonViewSet, AddonHistoryViewSet

router = DefaultRouter()

router.register(r'menu_structure', MenuStructureViewset, base_name="menu_structure_list")
router.register(r'addon', AddonViewSet, base_name="addon_list")
router.register(r'addon_history', AddonHistoryViewSet, base_name="addon_history_list")

urlpatterns = [
    url(r'^', include(router.urls)),
]
