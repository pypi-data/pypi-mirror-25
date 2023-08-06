# Author: Integra
# Dev: Partha.K

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .viewsets import QueryManagerViewSet, ModelRecords, DashBoardResults, QueryResults
from .viewsets import RequestQueryViewerViewSet

router = DefaultRouter()
router.register(r'query_manager',QueryManagerViewSet, base_name="query_manager_list")
router.register(r'request_query_viewer', RequestQueryViewerViewSet, base_name="request_query_viewer_list")

urlpatterns = [
    url(r'^', include(router.urls)),
    # Get all Page Related Models
    url(r'^model_records/$', ModelRecords.as_view()),
    # Dashboard Results URL
    url(r'^dashboard_results/$', DashBoardResults.as_view()),
    # QueryManager Dynamic Grid URL
    url(r'^query_results/', QueryResults.as_view()),    
]
