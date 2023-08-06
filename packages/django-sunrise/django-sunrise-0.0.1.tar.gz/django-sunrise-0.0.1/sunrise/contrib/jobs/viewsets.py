import pytz

from datetime import datetime
from sunrise.restful.viewsets import ViewSetManager as SunriseModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import ReqHeader, RequestBroadcast, ImportRequestDetail, ImportRequestDetailGrid, JobMessagesDtl, JobMessageHdr, GblProcess, GblProcMsgLog
from .serializers import ReqHeaderSerializer, RequestBroadcastSerializer, ImportRequestDtlSerializer, ImportRequestDtlGridSerializer, JobMessageHdrSerializer, JobMessagesDtlSerializer, GblProcessSerializer, GblProcMsgLogSerializer


class ReqHeaderViewSet(SunriseModelViewSet):
    model = ReqHeader
    parser = {
        'default': ReqHeaderSerializer,
    }

    def populate(self, request, context, mode):
        #context.update({'customer_id':'01'})
        #context.update({'program_id':'01'})        
        context.update({'audit_name':self.request.user.username})
        context.update({'audit_dttm':datetime.now()})
        return context

class RequestBroadcastViewSet(SunriseModelViewSet):
    parent = ReqHeader
    model = RequestBroadcast
    parser = {
        'default': RequestBroadcastSerializer
    }


class ImportRequestDtlViewSet(SunriseModelViewSet):
    parent = ReqHeader
    model = ImportRequestDetail
    parser = {
        'default': ImportRequestDtlSerializer
    }

class ImportRequestDtlGridViewSet(SunriseModelViewSet):
    parent = ReqHeader
    model = ImportRequestDetailGrid
    parser = {
        'default': ImportRequestDtlGridSerializer
    }


class JobMessageHdrViewSet(SunriseModelViewSet):
    model = JobMessageHdr
    
    parser = {
        'default': JobMessageHdrSerializer
    }

    def populate(self, request, context, mode):
        #context.update({'customer_id':'01'})
        context.update({'audit_name':self.request.user.username})
        context.update({'audit_dttm':datetime.now()})
        return context

class JobMessagesDtlViewSet(SunriseModelViewSet):
    parent = JobMessageHdr
    model = JobMessagesDtl
    parser = {
        'default': JobMessagesDtlSerializer
    }


class GblProcessViewSet(SunriseModelViewSet):
    model = GblProcess
    parser = {
        'default': GblProcessSerializer
    }

class GblProcMsgLogViewSet(SunriseModelViewSet):
    parent = GblProcess
    model = GblProcMsgLog
    parser = {
        'default': GblProcMsgLogSerializer
    }
