from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .viewsets import ReqHeaderViewSet, ImportRequestDtlViewSet, RequestBroadcastViewSet, ImportRequestDtlGridViewSet,JobMessageHdrViewSet, JobMessagesDtlViewSet, GblProcMsgLogViewSet, GblProcessViewSet

router = DefaultRouter()

router.register(r'request_hdr', ReqHeaderViewSet, base_name="request_hdr_list")
router.register(r'import_request_dtl', ImportRequestDtlViewSet, base_name="import_request_dtl")
router.register(r'request_broadcast', RequestBroadcastViewSet, base_name="request_broadcast")
router.register(r'import_request_dtl_grid', ImportRequestDtlGridViewSet, base_name="import_request_dtl_grid")
router.register(r'gbl_process', GblProcessViewSet, base_name="gbl_process")
router.register(r'gbl_proc_msg_log', GblProcMsgLogViewSet, base_name="gbl_proc_msg_log")
router.register(r'job_message_hdr', JobMessageHdrViewSet, base_name="job_message_hdr_list")
router.register(r'job_message_dtl', JobMessagesDtlViewSet, base_name="job_message_dtl_list")

urlpatterns = [
    url(r'^', include(router.urls)),
]
