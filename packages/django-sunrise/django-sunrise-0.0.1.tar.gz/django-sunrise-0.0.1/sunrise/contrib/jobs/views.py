import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, RequestContext
from django.conf import settings
from sunrise.pages.category import Category1
from .viewsets import ReqHeaderViewSet, RequestBroadcastViewSet, ImportRequestDtlViewSet, ImportRequestDtlGridViewSet, GblProcessViewSet, GblProcMsgLogViewSet 
from sunrise.contrib.jobs.job import Job, JobManager


class RequestHeader(Category1):
    parent = ReqHeaderViewSet
    childs = [
        (RequestBroadcastViewSet, 'grid', 'request_broadcast'),
        (ImportRequestDtlViewSet, 'normal', 'import_request_dtl'),  
        (ImportRequestDtlGridViewSet, 'grid', 'import_request_dtl_grid')
    ]

class ProcessTrack(Category1):
	parent = GblProcessViewSet
	childs = [
		(GblProcMsgLogViewSet, 'grid', 'gbl_proc_msg_log'),
	]
        
def data_import_task(request):
    kwargs = json.loads(request.body)['data']
    kwargs.update({'process_name':'DataImportProcess','user':request.user.username,'request_id':kwargs['request_nm']})
    JobManager(**kwargs)
    return HttpResponse("Ok")
