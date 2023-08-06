from django.db import models
from django.contrib.postgres.fields import JSONField

PROCESS_EXEC = (
    ('SUCCESS', 'SUCCESS'),
    ('WARNING', 'WARNING'),
    ('ERROR', 'ERROR'),
    ('CANCELLED','CANCELLED'),
    ('RUNNING','RUNNING'),
    ('QUEUED','QUEUED'),
)

MESSAGE_STATUS=(('Active','Active'),('Inactive','Inactive'))

MESSAGE_SEVERITY = (
    ('Success', 'Success'),
    ('Warning', 'Warning'),
    ('Error', 'Error'),
)

process_choices = (('Import Only','Import Only'),('Purge Only','Purge Only'),('Purge & Import','Purge & Import'))

data_type_choices = (('Cashbook Transactions','Cashbook Transactions'),('Custodial Transactions','Custodial Transactions'),('Break Transactions','Break Transactions'))
archive_method = (('Move','Move'),('Copy','Copy'),('Delete','Delete'))

ID_TYPE_CHOICES = (('USER', 'USER'),('ROLE', 'ROLE'),)
TYPE_CHOICES=(('Private','Private'),('Public','Public'))
STATUS_CHOICES=(('Active','Active'),('Inactive','Inactive'))
SCHEDULE_CHOICES=(('Initiated','Current Request is Initiated'),('Completed','Prior Request has Completed'),('Null','Null'))
HIDE_CHOICES=(('Y','Yes'),('N','No'))

class GblProcess(models.Model):
   process_id = models.CharField(unique=True,max_length=50,help_text='Process ID')
   request_id = models.CharField(max_length=50,help_text='Request ID')
   exec_program= models.CharField(max_length=60,help_text='Exec Program')
   exec_userid=  models.CharField(max_length=50,help_text='Exec UserId')
   exec_start_dttm=models.DateTimeField(blank = True,null = True,help_text='Start DateTime')
   exec_end_dttm=models.DateTimeField(blank = True, null = True,help_text='End DateTime')
   exec_status=models.CharField(max_length=10,choices=PROCESS_EXEC,help_text='Status')
   exec_params= models.CharField(max_length=400,help_text='Exec Params')

   def __unicode__(self):
       return str(self.process_id)
   class Meta:
       db_table='gbl_process'



class GblProcMsgLog(models.Model):
    tracking_id = models.AutoField(primary_key=True,help_text='Tracking ID')
    process_id = models.ForeignKey(GblProcess,help_text='Process ID_ID')
    request_id = models.CharField(max_length=20,help_text='Request ID')
    message_set= models.CharField(max_length=20,help_text='Message Set')
    message_id = models.CharField(max_length=20,help_text='Message ID')
    severity = models.CharField(max_length=10,help_text='Severity')
    message_text=models.CharField(max_length=50,help_text='Text Message')
    explanation = models.CharField('Explanation', max_length=1024,help_text='Explanation')
    class Meta:
       db_table='gbl_proc_msg_log'



class JobMessageHdr(models.Model):
    id = models.AutoField(primary_key=True,help_text='ID')
    message_set = models.CharField(help_text='Message Set',max_length=10)
    set_description = models.CharField(help_text='Description', max_length=30)
    audit_name=models.CharField(max_length=30,null=True,help_text='Audit Name')
    audit_dttm=models.DateTimeField(null=True,blank=True,help_text='Audit DateTime')

    def __unicode__(self):
        return self.id

    class Meta:
        db_table='gbl_messages_hdr'
        #unique_together = ('customer_id', 'message_set')
        
    def clean(self):
        if self.message_set in [None,'']:
            raise ValidationError("Message Set Is Required")


class JobMessagesDtl(models.Model):
    id = models.AutoField(primary_key=True,help_text='Sequence ID')
    message_id= models.CharField(max_length=50,help_text='Message ID')
    message_set=models.ForeignKey(JobMessageHdr,help_text='MessageSet_ID', related_name = "message_dtl")
    status=models.CharField(max_length=10,choices=MESSAGE_STATUS,default='Active',help_text='Status')
    severity=models.CharField(max_length=10,choices=MESSAGE_SEVERITY,default='Success',help_text='Severity')
    broadcast = models.CharField(max_length=50,help_text='Broadcast')
    message_text=models.CharField(max_length=50,help_text='Message')
    explanation = models.CharField(help_text='Explanation', max_length=1024)

    def __unicode__(self):
        return str(self.sequence)
    class Meta:
        db_table='sunrise_contrb_job_message_dtl'

class ReqHeader(models.Model):
    #customer_id = models.CharField(max_length=50,help_text='Customer ID')
    id = models.AutoField(primary_key=True,help_text='ID')
    request_nm = models.CharField(max_length=50,help_text='Request ID')
    description = models.CharField(help_text='Description:',max_length=20)
    type = models.CharField(help_text='Type:',max_length=20,choices=TYPE_CHOICES,default='Private')
    status = models.CharField(help_text='Status',max_length=20,choices=STATUS_CHOICES,default='Active')
    hide= models.CharField(max_length=3,choices=HIDE_CHOICES,default='N',blank=True,null=True,help_text='')
    program_id=models.CharField(max_length=50,help_text='Program ID')
    schedule_request=models.BooleanField(default=False,help_text='Schedule Request')
    schedule_next=models.CharField(max_length=20,choices=SCHEDULE_CHOICES,blank=True,null=True,default='Initiated',help_text='Schedule Next Request When')
    start_date=models.DateField(blank=True, null=True,help_text='Start Date')
    start_time=models.TimeField(blank=True, null=True,help_text='Start Time')
    end_date=models.DateField(blank=True, null=True,help_text='Start Date')
    end_time=models.TimeField(blank=True, null=True,help_text='End Time')
    run_clndr_id=models.CharField(max_length=50,blank=True, null=True,help_text='Run On Calendar')
    run_sch_days=models.IntegerField(blank=True, null=True,help_text='Run on Schedule Days')
    no_run_clndr_id=models.CharField(max_length=50,blank=True, null=True,help_text='Do Not Run On Calendar')
    no_run_clndr_year=models.CharField(max_length=5,blank=True, null=True,help_text='Do Not Run On Calendar year')
    no_run_sch_days=models.IntegerField(blank=True, null=True,help_text='Do Not Run on Schedule Days')
    clndr_conflict_res=models.CharField(max_length=5,blank=True, null=True,help_text='Calendar Conflict Result')
    audit_name=models.CharField(help_text='Audit Name',max_length=30)
    audit_dttm=models.DateTimeField(help_text='Audit DateTime')
    run_name=models.CharField(max_length=30,blank=True, null=True,help_text='Last Run By')
    run_dttm=models.DateTimeField(blank=True, null=True,help_text='Last Run DateTime')

    class Meta:
       db_table='sunrise_contrb_job'
       unique_together = (("request_nm","type","program_id"),)

    def clean(self):
        if self.request_nm in [None,'']:
            raise ValidationError("Request ID Is Required")

class RequestBroadcast(models.Model):
    request_id = models.ForeignKey(ReqHeader,help_text='Job ID_ID')
    id_type = models.CharField(max_length=6,choices=ID_TYPE_CHOICES,help_text='ID Type',default='USER')
    broadcast_rcpt = models.CharField(max_length=50,help_text='Broadcast ID')
    error = models.BooleanField(default=False,help_text='On Error')
    warning = models.BooleanField(default=False,help_text='On Warning')
    success = models.BooleanField(default=False,help_text='On Success')
    disabled = models.BooleanField(default=False,help_text='Disabled')

    class Meta:
        db_table='sunrise_contrb_job_broadcast'



class ImportRequestDetail(models.Model):
    request_id= models.ForeignKey(ReqHeader,help_text='Request ID_ID')
    process_options = models.CharField(max_length=20,choices=process_choices,default='Import Only',help_text='Request Process Options')
    calendar_id = models.CharField(max_length=30,blank=True, null= True,help_text='Calendar ID')
    year = models.CharField(max_length=4,blank=True,null=True,help_text='Year')
    cutoff_date = models.DateField(blank=True,null=True,help_text='Cut Off Date')
    import_id = models.CharField(max_length=110,blank=True,null=True,help_text='Import ID')
    import_data_error = models.BooleanField(default=False,help_text='Do not import data on error or warning')
    data_type = models.CharField(max_length=40,choices=data_type_choices,blank=True, null= True,help_text='Data Type')
    class Meta:
        db_table = "imp_request_detail"        


class ImportRequestDetailGrid(models.Model):
    id = models.AutoField(primary_key=True,help_text='Sequence Number')
    request_id= models.ForeignKey(ReqHeader,help_text='Job ID')
    format_id = models.CharField(max_length=20,help_text='Format ID')
    data_type = models.CharField(max_length=40,blank=True, null= True,help_text='Data Type')
    file_path = models.TextField(help_text='File Location')
    file_name = models.CharField(max_length=100,help_text='File Name')
    archive_method = models.CharField(max_length=8,default='Move',help_text='Archive Method',choices=archive_method)
    archive_path = models.TextField(blank=True,null= True,help_text='Archive Location')
    sheet_name = models.CharField(max_length=20,default='Sheet1',help_text='Sheet Name')
    header_row = models.IntegerField(default=1,help_text='Header Row')
    skip_row_top = models.IntegerField(default=0,help_text='Skip Row Top')
    skip_row_bottom = models.IntegerField(default=0,help_text='Skip Row Bottom')
    class Meta:
        db_table = "imp_request_detail_grid"

class MasterSourceData(models.Model):
    id = models.AutoField(primary_key=True,help_text='Sequence Number')
    investor_id = models.CharField(max_length=40,help_text='Investor ID')
    loan_id = models.CharField(max_length=40,help_text='Loan ID')
    cutoff_date = models.DateField(blank=True,null=True,help_text='Cutoff Date')
    data = JSONField(null = True)

    class Meta:
        db_table = "master_source_data"




