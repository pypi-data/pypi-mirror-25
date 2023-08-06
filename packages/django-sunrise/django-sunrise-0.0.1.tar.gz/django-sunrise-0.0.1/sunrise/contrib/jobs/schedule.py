from datetime import datetime, date, time, timedelta
import pytz
from django.conf import settings
tz = pytz.timezone(settings.TIME_ZONE)

from celery.contrib import rdb

def schedulesub(request_id,eta):
    from sunrise.contrib.jobs.models import ReqHeader
    from setup.models import Calendar

    def get_eta_dt(dt,cal,ncal,hdr):
        week_day=dt.weekday()+1
        runons=cal.runon.values_list('day_id',flat=True) 
        if week_day in runons:
            rdt=dt
        else:
            if week_day > max(runons):
                next_day=min(runons)
                rdt=dt+timedelta(days=(7-week_day)+next_day)
            else:
                for runon in runons:
                    if week_day < runon:
                        next_day=runon
                        break
                rdt=dt+timedelta(days=next_day-week_day)
        if ncal:
            hdts=ncal.calendardate_set.all().values_list('from_date','to_date')
            nrun=filter(lambda x:bool(x),[x[0]<=rdt<=x[1] for x in hdts])
            if bool(nrun):
                rdt=get_eta_dt(dt+timedelta(days=1),cal,ncal,hdr)
        return rdt

    hdr = ReqHeader.objects.get(request_nm=request_id)
    tz = pytz.timezone(settings.TIME_ZONE)
    current_dttm = tz.localize(datetime.now())
    curr_dt = current_dttm.date()
    curr_tm = current_dttm.time()
    if hdr.run_clndr_id==None or hdr.run_clndr_id=='':
        eta = tz.localize(datetime(hdr.start_date.year, hdr.start_date.month, hdr.start_date.day, hdr.start_time.hour,hdr.start_time.minute,hdr.start_time.second))
    else:
        cal = Calendar.objects.get(calendar_nm= hdr.run_clndr_id)
        ncal=None
        if hdr.no_run_clndr_id!=None and hdr.no_run_clndr_id!='':
            ncal = Calendar.objects.get(calendar_nm= hdr.no_run_clndr_id, year= hdr.no_run_clndr_year)
        if curr_dt < hdr.start_date:
            eta_dt = get_eta_dt(hdr.start_date,cal,ncal,hdr)
        else:
            eta_dt = get_eta_dt(curr_dt,cal,ncal,hdr)
        eta_tm = hdr.start_time          
        if curr_tm > hdr.start_time:
            if cal.recurring_for:  
                delta = timedelta(hours=cal.recurring_for) if cal.recurring_for_units == 'H' else timedelta(minutes=cal.recurring_for)
                temp_end_time = (datetime.combine(datetime.now().date(), hdr.start_time)+delta).time()
                if curr_tm < temp_end_time:
                    eta_dt = curr_dt
                    delta = timedelta(hours=cal.recurring_evry) if cal.recurring_evry_units == 'H' else timedelta(minutes=cal.recurring_evry)
                    eta_tm = (datetime.combine(datetime.now().date(), curr_tm)+delta).time()
                else:
                    eta_dt = get_eta_dt(curr_dt+timedelta(days=1),cal,ncal,hdr)
                    eta_tm = hdr.start_time
            else:
                eta_dt = get_eta_dt(curr_dt+timedelta(days=1),cal,ncal,hdr)
                eta_tm = hdr.start_time
        eta = tz.localize(datetime(eta_dt.year, eta_dt.month, eta_dt.day, eta_tm.hour, eta_tm.minute, eta_tm.second))
    if hdr.end_date:
        if eta.date() > hdr.end_date:
            eta=None
        elif eta.date == hdr.end_date:
            if hdr.end_time and eta.time() > hdr.end_time:
                eta=None
    return eta


# def schedule_process(func):
#     @wraps(func)
#     def inner(*args,**kwargs):
#         request_id=args[0]
#         process=kwargs['process']
#         task_request_id=kwargs['task_request_id']
#         request_hdr = ReqHeader.objects.get(pk=request_id)
#         kwargs['req_header']=request_hdr
#         import_dict = {
#             'File Import Process' : ['cashbook.bookvalues.models','ImportRequestDetail']
#         }
        
#         if process in import_dict:
#             model_path, model_name = import_dict[process]
#             model_class = getattr(import_module(model_path), model_name)
#             model_ins = model_class.objects.get(request_id=request_hdr)
#             kwargs['req_detail']=model_ins            
#             if model_ins.request_id.schedule_request==True and model_ins.request_id.run_clndr_id:
#                 if model_ins.request_id.schedule_next== 'Y':
#                     kwargs.update({'request_id':request_id,'task_id':task_request_id,'schedule_next_flag':True})
#                     from core.config.process_manager import process_manager
#                     process_manager(**kwargs)
#                 elif model_ins.request_id.schedule_next== 'N':
#                     if 'schedule_next_flag' in kwargs:
#                         del kwargs['schedule_next_flag']
#                     from celery import current_task
#                     current_task.request.kwargs['request_id']=request_id
#                     current_task.request.kwargs['schedule_after_success']=True
#         return func(*args,**kwargs)
#     return inner
