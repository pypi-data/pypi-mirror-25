# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from .views import UserLogin, UserLogout

urlpatterns = [
    #UserLogin
    url(r'^login/$', UserLogin.as_view()),
    #UserLogout
    url(r'^logout/$', UserLogout),    
]
