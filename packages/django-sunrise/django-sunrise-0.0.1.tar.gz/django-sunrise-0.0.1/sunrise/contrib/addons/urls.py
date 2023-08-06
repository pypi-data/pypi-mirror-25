# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from .views import AddonPage, MenuBuilder

urlpatterns = [
    url(r'^setup/addon/(?P<dispatch>[\w-]+)/$', AddonPage.as_view(template = "addon.html")),
    url(r'^setup/menu_builder/(?P<dispatch>[\w-]+)/$', MenuBuilder.as_view(template = "menu_builder.html")), 
]
