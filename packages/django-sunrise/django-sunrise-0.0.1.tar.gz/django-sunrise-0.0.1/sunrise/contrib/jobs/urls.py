from django.conf.urls import include, url

from .views import RequestHeader, ProcessTrack

urlpatterns = [
    #Request Transaction Import
    url(r'^request_transaction_import/(?P<dispatch>[\w-]+)/$', RequestHeader.as_view(template = "importrequest.html")),
    url(r'^process_track/(?P<dispatch>[\w-]+)/$', ProcessTrack.as_view(template = "process_track.html")),

]