from datetime import datetime

from rest_framework import serializers as baseserializer
from rest_framework_hstore.fields import HStoreField

from sunrise.restful import serializers
from sunrise.restful.serializers import NormalSerializer, GridSerializer
from .models import ReqHeader,ImportRequestDetail,RequestBroadcast,ImportRequestDetailGrid, JobMessageHdr, JobMessagesDtl, GblProcess, GblProcMsgLog


class ReqHeaderSerializer(NormalSerializer):
    class Meta:
        model = ReqHeader

class ImportRequestDtlSerializer(NormalSerializer):
    class Meta:
        model = ImportRequestDetail

class RequestBroadcastSerializer(GridSerializer):
	class Meta:
		model = RequestBroadcast

class ImportRequestDtlGridSerializer(GridSerializer):
    class Meta:
        model = ImportRequestDetailGrid

class JobMessageHdrSerializer(NormalSerializer):
    class Meta:
        model = JobMessageHdr


class JobMessagesDtlSerializer(GridSerializer):
    class Meta:
        model = JobMessagesDtl        


class GblProcessSerializer(NormalSerializer):
    class Meta:
        model = GblProcess

class GblProcMsgLogSerializer(GridSerializer):
    class Meta:
        model = GblProcMsgLog
