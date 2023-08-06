from celery.task import Task
from datetime import datetime
from celery import shared_task
from .signals import process_logger,message_logger
import pytz,time
from django.conf import settings
from .schedule import schedulesub
tz = pytz.timezone(settings.TIME_ZONE)

from celery.contrib import rdb

def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses

class MessageLogger(object):

    def logSuccess(self, message):
        pass

    def logError(self, message):
        pass

    def logWarning(self, message):
        pass


class JobNotyManager(object):

    def __init__(self, *args, **kwargs):
        pass

    def _sendNoty(self, process_id, request_id, _from, _to, subject, message, data, status):
        """ Used to send the noty to the client using tornado """
        from sunrise.contrib.notifications.views import ProcessNotifier
        processObj = ProcessNotifier(process_id, request_id).From(_from).To(_to).Subject(subject).Body(message).Data(message)
        getattr(processObj,status.title())()
        return True

    def updateNotfy(self, process_id, status):
        """ Used to update the status of the existing noty """
        #1. Get respective ProcessObj
        from sunrise.contrib.jobs.models import GblProcess,GblProcMsgLog
        try:
            procObj = GblProcess.objects.get(process_id = process_id)
        except GblProcess.DoesNotExist:
            time.sleep(2)  
        procObj = GblProcess.objects.get(process_id = process_id)     

        if status in ['Error','Failure','Success']:
            if GblProcMsgLog.objects.filter(process_id=process_id, severity ='Warning').exists() and status!='Failure':
                status = 'Warning'
            if GblProcMsgLog.objects.filter(process_id=process_id, severity ='Error').exists() and status!='Error':
                status = 'Error'            
            if status == 'Failure':
                status = 'Error'
            procObj.exec_end_dttm = tz.localize(datetime.now())
        procObj.exec_status = status
        procObj.save()
        #2. Send noty to the client
        self._sendNoty(procObj.process_id, procObj.request_id, procObj.exec_userid, procObj.exec_userid, procObj.exec_program, procObj.exec_program, procObj.exec_params, status)
        return True        

    def createNotfy(self, user=None, process_name=None, process_id=None, request_id=None, start_time=None, end_time=None, exec_params={}, status=None):
        """ Used to create status for new process """
        assert user is not None, "User name should not be None"
        assert process_name is not None, "Process Name should not be None"
        assert status is not None, "Status should not be None"
        # import pdb;pdb.set_trace()
        if start_time is None:
            start_time = tz.localize(datetime.now())
        payload = {
            'request_id': request_id,
            'process_id':process_id,
            'exec_program':process_name,
            'exec_userid':user,
            'exec_start_dttm':start_time,
            'exec_end_dttm':end_time,
            'exec_status':status,
            'exec_params':exec_params
        }
        from sunrise.contrib.jobs.models import GblProcess
        procObj = GblProcess.objects.create(**payload)
        self._sendNoty(process_id, request_id, user, user, process_name, process_name, exec_params, status)
        return True
    

class JobManager(object):

    def __init__(self, 
                    process_name = None,
                    request_id = None,
                    user = None,
                    initial = False,
                    **kwargs
                    ):

        self.process_name = process_name
        self.request_id = request_id
        self.user = user
        self.initial = initial
        self.kwargs = kwargs
        self.initializeJobNumber()
        self.initiateJob()
        

    def initiliseKwargs(self):
        self.kwargs['process_number'] = self.process_number
        self.kwargs['process_name'] = self.process_name
        self.kwargs['request_id'] = self.request_id
        self.kwargs['user'] = self.user
        self.kwargs['initial'] = self.initial
        self.asyncKwargs = {}
        self.asyncKwargs['args'] = None
        self.asyncKwargs['kwargs'] = self.kwargs 
        self.asyncKwargs['eta'] = self.estimatedEta()
        self.asyncKwargs['task_id'] = self.process_number

    def initializeJobNumber(self):
        initial_process_id = 100000
        from sunrise.contrib.jobs.models import GblProcess
        try:
            processObj = GblProcess.objects.latest('pk')
            process_number = int(processObj.process_id) + 1
        except GblProcess.DoesNotExist:
            process_number = initial_process_id
        self.process_number = str(process_number)

    def estimatedEta(self):
        from sunrise.contrib.jobs.models import ReqHeader
        request = ReqHeader.objects.get(request_nm=self.request_id)
        current_dttm = tz.localize(datetime.now())        
        if request.schedule_request:
            eta = datetime(current_dttm.year,current_dttm.month,current_dttm.day,current_dttm.hour,current_dttm.minute,current_dttm.second)
            return schedulesub(self.request_id,eta)
        else:
            return current_dttm

    def initiateJob(self):
        task = globals()[self.process_name]
        self.initiliseKwargs()
        task.apply_async(**self.asyncKwargs)


class Job(Task):    
    
    BROADCAST = True

    def run(self, to):
        return 'hello {0}'.format(to)

    def configProcess(self, **kwargs):
        self.process_number = kwargs['process_number']
        self.process_name = kwargs['process_name']
        self.request_id = kwargs['request_id']
        self.user = kwargs['user']
        self.logger = process_logger(kwargs['process_number'])

    def msgLog(self,message_set, message_id, **msgArgs):
        message_logger(self.process_number,self.request_id, message_set, message_id, self.logger, **msgArgs)

    def onRunning(self, **kwargs):
        payload = {
            'process_id':kwargs['process_number'],
            'status':'Running'
        }
        JobNotyManager().updateNotfy(**payload)

    def onCompleted(self,job_exec_status, **kwargs):  
        payload = {
            'process_id':kwargs['process_number'],
            'status':job_exec_status.title()
        }
        JobNotyManager().updateNotfy(**payload)
        self.msgLog('Gen','S999',**{'process':self.process_name,'status':job_exec_status})
    
    def scheduleNext(self, **kwargs):
        from sunrise.contrib.jobs.models import ReqHeader
        request = ReqHeader.objects.get(request_nm=kwargs['request_id'])
        if request.schedule_request:
            schedule_next = request.schedule_next
            if schedule_next== 'Initiated':
                JobManager(**kwargs)
            elif schedule_next== 'Completed':
                if 'schedule_next_flag' in kwargs:
                    del kwargs['schedule_next_flag']
                from celery import current_task
                current_task.request.kwargs['schedule_after_success']=True

    def scheduleAfterSuccess(self,state, **kwargs):
        if 'schedule_after_success' in kwargs and kwargs['schedule_after_success'] and state=='SUCCESS':
            JobManager(**kwargs)


class ProcessBillingTask(Job):
    name = "process_billing_task"
    def run(self, **kwargs):  
        from process_billing.process import process_billing        
        self.configProcess(**kwargs) 
        self.msgLog('Gen','S000',**{'process':self.process_name})
        process_billing(**kwargs)
        
class DataImportProcess(Job):
    name = "data_import_process"
    def run(self, **kwargs):  
        from billing.dataimport import dataimport
        self.configProcess(**kwargs) 
        self.msgLog('Gen','S000',**{'process':self.process_name})
        kwargs['logger']=self.logger
        dataimport(**kwargs)

class FtpSyncScheduler(Job):
    name="request_ftp_scheduler"
    def run(self, **kwargs):    
        from sunrise.contrib.cloud.sync_ftp_s3 import FTPScheduler
        self.configProcess(**kwargs)
        try:
            self.msgLog('Gen','S000',**{'process':self.process_name})
        except Exception as e:
            print e
        kwargs['logger']=self.logger
        FTPScheduler(**kwargs)    

