# Author: Integra
# Dev: Partha
# Description: Logic for querymanager
import json

from django.http import HttpResponse

from sunrise.pages.category import Category1
from sunrise.pages.category import Category2

from sunrise.contrib.jobs.viewsets import ReqHeaderViewSet
from .viewsets import QueryManagerViewSet, RequestQueryViewerViewSet

class QueryManager(Category1):
    parent = QueryManagerViewSet
    childs = []

class QueryViewer(Category2):
    childs = [
        (QueryManagerViewSet, 'query_viewer')
    ]

class QueryScheduler(Category1):
    parent = ReqHeaderViewSet
    childs = [
        (RequestQueryViewerViewSet, 'normal', 'request_query_scheduler'), 
    ]

def request_query_scheduler(request):
    assert(request.body is not None), "Insufficient data"
    _input = json.loads(request.body)
    HdrData = _input['data']
    QueryData_ = _input['detail']
    return HttpResponse("Ok")