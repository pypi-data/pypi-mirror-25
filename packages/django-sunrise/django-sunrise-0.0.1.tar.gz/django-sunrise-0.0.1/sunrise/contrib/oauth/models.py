# Author: Integra
# Dev: Partha(Ref)

from django.db import models

from oauth2_provider.models import Application

""" Used to hold the resource level permission """
class AppResourcePermission(models.Model):
    appID = models.ForeignKey(Application, related_name = "oauth_permission")
    api_url = models.TextField()
    can_list = models.BooleanField(default = True)
    can_retrieve = models.BooleanField(default = True)
    can_create = models.BooleanField(default = False)
    can_update = models.BooleanField(default = False)
    can_destroy = models.BooleanField(default = False)

    class Meta:
        db_table = "sunrise_contrib_oauth_app_resource_permission"


class RequestHandshake(models.Model):
    url = models.TextField()
    from_origin = models.CharField(max_length = 100)
    access_key = models.CharField(max_length = 100, null=True)
    secret_key = models.CharField(max_length = 100, null=True)
    status = models.CharField(max_length = 50)
    requested_on = models.DateField(auto_now_add = True)
    REF_CODE = models.CharField(max_length = 30, null = True)
    counterparty = models.CharField(max_length = 50, null = True)
    class Meta:
        db_table = "request_hand_shake"

