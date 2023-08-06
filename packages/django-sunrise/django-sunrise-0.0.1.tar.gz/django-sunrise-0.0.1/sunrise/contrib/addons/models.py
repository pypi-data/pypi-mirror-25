# Author: Integra
# Dev: Partha(Ref)

from django.db import models
from django.contrib.postgres.fields import HStoreField


""" To store the menu """
class MenuStructure(models.Model):
    data = HStoreField(null = True)

    class Meta:
        db_table = "menu_structure"

""" To store the Addons """
class Addon(models.Model):
    name = models.CharField(max_length = 50)
    version = models.CharField(max_length = 5)
    location = models.CharField(max_length = 150)
    description = models.CharField(max_length = 100)
    type = models.CharField(max_length = 30)
    reviewer = models.CharField(max_length = 100)
    comment = models.CharField(max_length = 100, null=True)
    test_cases = models.CharField(max_length = 150, null=True)
    status = models.CharField(max_length = 30)
    review_status = models.CharField(max_length = 150, null = True)

    submitted_on = models.DateTimeField(auto_now_add = True)
    request_for_deployment_on = models.DateTimeField(null = True)
    deployed_on = models.DateTimeField(null = True)
    reviewed_on = models.DateTimeField(null = True)

    submitted_by = models.CharField(max_length = 100, null = True)
    reviewed_by = models.CharField(max_length = 100, null = True)
    deployed_by = models.CharField(max_length = 100, null = True)

    data = HStoreField(null = True)

    class Meta:
        db_table = "addon"

""" To keep track of the auditing of the plugin """
class AddonHistory(models.Model):
    addon = models.ForeignKey(Addon)
    audit_dttm = models.DateTimeField(auto_now_add = True)
    audit_user = models.CharField(max_length = 100)
    data = HStoreField(null = True)

    class Meta:
        db_table = "addon_history"




    