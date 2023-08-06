# Author: Integra
# Dev: Partha
# Description: Page&Supporting Func

from django.conf.urls import include, url
from .views import  QueryManager
from .views import  QueryViewer
from .views import QueryScheduler

urlpatterns = [
    # QueryManager Builder(Page URL)
    url(r'^query_manager/(?P<dispatch>[\w-]+)/', QueryManager.as_view(template = "query_manager.html")),  
    # QueryViewer 
    url(r'^query_viewer/(?P<dispatch>[\w-]+)/', QueryViewer.as_view(template = "query_viewer.html")),  
    # QueryViewer 
    url(r'^query_scheduler/(?P<dispatch>[\w-]+)/', QueryScheduler.as_view(template = "query_scheduler.html")),  
]
