# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from .views import OauthApplicationiView, RequestHandshakeView

urlpatterns = [
    #Define Oauth
    url(r'^define_oauth_access/(?P<dispatch>[\w-]+)/$', OauthApplicationiView.as_view(template = "app_resource_permissions.html")),
    #Define Handshake Access
    url(r'^define_portal_handshake/(?P<dispatch>[\w-]+)/$', RequestHandshakeView.as_view(template = "define_portal_handshake.html")),    
]
