from django.db import models
from django.contrib.postgres.fields import JSONField

from sunrise.contrib.jobs.models import ReqHeader

class QueryManager(models.Model):

    TYPE_CHOICES=(
        ('',''),
        ('Private','Private'),
        ('Public','Public')
        )

    name = models.CharField(max_length=50,unique=True)
    qtype = models.CharField(max_length=20,choices=TYPE_CHOICES, default='Private')
    description = models.CharField(max_length=100)
    effective_from = models.DateTimeField(help_text='Effective From',blank=True,null=True)
    expression = JSONField()
    records = JSONField()
    relations = JSONField()
    fields = JSONField()
    criteria = JSONField()
    summary = models.TextField()
    subqueries = JSONField(null = True)
    has_limit = models.BooleanField(default = False)
    limit_range = models.CharField(null = True, blank = True, max_length = 5)
    select_distinct = models.BooleanField(default = False)

    class Meta:
        db_table = 'query_manager'


class RequestQueryViewer(models.Model):
    request_id= models.ForeignKey(ReqHeader)
    query_name = models.CharField(max_length=30)
    query_description = models.CharField(max_length=60)
    query_summary = models.TextField()
    file_name = models.TextField(max_length=100)

    class Meta:
        db_table = 'request_query_viewer'