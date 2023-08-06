from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField

from sunrise.contrib.authentication.models import SunriseProfile as User


BROADCAST_TYPE_CHOICES = (('1', 'Processing'),('2', 'Message'),('3', 'Notification'))
PROCESS_EXEC = (
    ('SUCCESS', 'SUCCESS'),
    ('WARNING', 'WARNING'),
    ('ERROR', 'ERROR'),
    ('CANCELLED','CANCELLED'),
    ('RUNNING','RUNNING'),
    ('QUEUED','QUEUED'),
)
MESSAGE_CHOICES = (('READ', 'READ'),('UNREAD', 'UNREAD'),('DELETED', 'DELETED'),)


class Broadcast(models.Model):
    """ Tracking the messages which are broadcasting in the system """
    broadcast_id = models.AutoField(primary_key=True,max_length=10,help_text='ID')
    #Boradcast type
    broadcast_type = models.CharField(choices=BROADCAST_TYPE_CHOICES, default='1',max_length=2,help_text='Broadcast Type')
    #Message Audit Details
    sender = models.CharField(max_length = 100, null=True, help_text='Broadcast Sender')
    receiver = models.CharField(max_length = 100, null=True, help_text='Broadcast Receiver')
    #Message Tracking ID
    process_id = models.CharField(max_length=50,blank=True,null=True,help_text='Process ID')
    request_id = models.CharField(max_length=50,blank=True,null=True,help_text='Request ID')
    #Process tracking
    queued_at = models.DateTimeField(blank=True,null=True,help_text='Queued Start')
    running_at = models.DateTimeField(blank=True,null=True,help_text='Running Start')
    terminated_at = models.DateTimeField(blank=True,null=True,help_text='terminated Start')
    success_at = models.DateTimeField(blank=True,null=True,help_text='Success Start')
    cancelled_at = models.DateTimeField(blank=True,null=True,help_text='Canceld Start')
    #Execution Status
    exec_status = models.CharField(max_length=10,choices=PROCESS_EXEC,help_text='Exec Status')
    #Message Template
    message_hdr = models.CharField(max_length=60,help_text='Broadcast Header')
    message_dtl = models.CharField(max_length=200,help_text='Broadcast Detail')
    message_data = models.TextField(u"text",max_length=35,help_text='Message Data')
    #Message Audit
    message_dttm = models.DateTimeField(u"created at",help_text='Message DateTime')
    #Message Status(Read/Unread/deleted)
    message_status = models.CharField(max_length=10,choices=MESSAGE_CHOICES, default='UNREAD',help_text='')

    class Meta:
        db_table = "sunrise_contrib_notifications_broadcasts"


class UserPreferences(models.Model):
    username = models.CharField(max_length = 100)
    data = JSONField(null = True)

    class Meta:
        db_table = "user_preferences"


class UserTheme(models.Model):
    name = models.CharField(max_length = 30)
    data = JSONField(null = True)

    class Meta:
        db_table = "user_theme"
