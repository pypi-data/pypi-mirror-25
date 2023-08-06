# Author: Integra
# Dev: Partha(Ref)

from django.conf.urls import include, url

from .views import UserPage, DefineRoles, DefineUsers

urlpatterns = [
    #Define Users
    url(r'^define_users/(?P<dispatch>[\w-]+)/$', DefineUsers.as_view(template = "define_users.html")),
    #Define Page Groups
    url(r'^define_page_groups/(?P<dispatch>[\w-]+)/$', UserPage.as_view(template = "define_page_groups.html")),
    #Define Roles
    url(r'^define_roles/(?P<dispatch>[\w-]+)/$', DefineRoles.as_view(template = "define_roles.html")),
    #Define Customers
    url(r'^customer_details/(?P<dispatch>[\w-]+)/$', UserPage.as_view(template = "customer_details.html")),
]
