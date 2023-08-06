# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from .views import CloudView

urlpatterns = [
    url(r'^read/$', CloudView.as_view()),
    url(r'^write/$', CloudView.as_view()),
    url(r'^delete/$', CloudView.as_view()), 
    url(r'^download/$', CloudView.as_view()),       
]
