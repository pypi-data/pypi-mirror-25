from celery.signals import after_task_publish,task_prerun,task_postrun,task_failure
from celery.contrib import rdb
from django.conf import settings
import logging
import os
from datetime import datetime


def import_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

@after_task_publish.connect
def after(headers=None,body=None,exchange=None,routing_key=None,signal=None,sender=None, **kwg):
    bodyAgrs = body[1]
    from sunrise.contrib.jobs.job import JobNotyManager
    payload = {
        'user': bodyAgrs['user'], 
        'process_name': bodyAgrs['process_name'],
        'process_id': bodyAgrs['process_number'],
        'request_id': bodyAgrs['request_id'],
        'start_time':None,
        'end_time':None,
        'exec_params': { key : bodyAgrs[key] for key in ['process_number','process_name','request_id','user'] },
        'status':'Queued'
    }
    JobNotyManager().createNotfy(**payload)

@task_prerun.connect
def running(task_id=None,task=None,args=None,kwargs=None,signal=None,sender=None, **kwg):
    sender.scheduleNext(**kwargs)
    sender.onRunning(**kwargs)    
    
@task_postrun.connect
def completed(task_id=None,task=None,args=None,kwargs=None,retval=None,state=None,sender=None, **kwg):
    sender.scheduleAfterSuccess(state, **kwargs)
    sender.onCompleted(state, **kwargs)
        

@task_failure.connect
def failure(task_id=None, exception=None,args=None, kwargs=None, traceback=None, einfo=None, **kwg):  
    print exception
    #sender.onCompleted('Failure', **kwargs)
    

def close_process(exitor,process_number,request_id):
    if exitor:
        from celery import current_task
        current_task.request.kwargs['exit_with_error']=True
        raise Exception("Redirect to Failure")
    else:
        pass
        # PROJECT_ROOT = settings.PROJECT_ROOT
        # logfile = PROJECT_ROOT.child('media') +"/logs/"+ processid+".log"
        # s3_logfile = "media/logs/"+processid +'.log'
        # buck = aws_s3()
        # k = Key(buck)
        # k.key = s3_logfile
        # try:
        #     k.set_contents_from_filename(logfile)
        #     if os.path.isfile(logfile):
        #         os.system("rm "+logfile)
        # except IOError:
        #     pass
        # if exit == 'Failure':
        #     process_log(processid,request_id, "Gen", "S999", **{'process':task_nm,'status':'abruptly'})
        # else:
        #     process_log(processid,request_id, "Gen", "S999", **{'process':task_nm,'status':'normally'})


def message_logger(process_id, request_id, message_set, message_id, logger, syslog=True, filelog=True,custom_explanation=False, **kwargs):
    from .models import JobMessagesDtl,GblProcess,GblProcMsgLog
    gmd = JobMessagesDtl.objects.get(message_set__message_set = message_set, message_id = message_id)
    gp = GblProcess.objects.get(process_id = process_id)
    explanation =str(datetime.now())+": "+gmd.explanation%kwargs
    if syslog:
        msgArgs = { 'process_id': gp, 'request_id':request_id, 'message_set':message_set, 'message_id':message_id,'severity': gmd.severity, 'message_text': gmd.message_text, 'explanation': explanation }
        GblProcMsgLog.objects.create(**msgArgs)
    if filelog:
        logger.info(custom_explanation if custom_explanation else gmd.explanation%kwargs)


def process_logger(process_id):
    PROJECT_ROOT=settings.PROJECT_ROOT
    logger = logging.getLogger(process_id)
    if not os.path.isdir(PROJECT_ROOT.child('media') + '/logs/'):
        os.makedirs(PROJECT_ROOT.child('media') + '/logs/')
    fname= PROJECT_ROOT.child('media') + '/logs/' + process_id +'.log'
    hdlr = logging.FileHandler(fname)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger
