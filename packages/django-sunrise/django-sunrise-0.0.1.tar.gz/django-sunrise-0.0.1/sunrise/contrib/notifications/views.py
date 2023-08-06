from django.shortcuts import render
from django.http import HttpResponse
import json
from datetime import datetime
from celery.contrib import rdb
from .models import Broadcast
from django.conf import settings
from django.views.generic import View

from .models import UserPreferences, UserTheme

class Notifier(object):
    """ Base notifier to broadcast Messages/Process/Notification type messages to clients asyncly """
    sender = None
    receiver = None
    message_hdr = None
    message_dtl = None

    def __init__(self, *args, **kwargs):
        pass

    def _validate(self,*args, **kwargs):
        def wrapper(self):
            assert(self.sender is not None), "From should not be empty"
            assert(self.receiver is not None), "To should not be empty"
            assert(self.message_hdr is not None), "Subject should not be empty"
            assert(self.message_dtl is not None), "Body should not be empty"
        return wrapper
    
    def get_or_create(self, data):
        """ Will Create Broadcast Object with the specified data """
        # rdb.set_trace()
        try:
            Obj = Broadcast.objects.get(process_id = data['process_id'])
        except Broadcast.DoesNotExist:
            Obj, created = Broadcast.objects.get_or_create(**data)
            return Obj
        return Obj

    def getNotificationCount(self, user):
        """ Return Notification Count of each type of specific user """
        objs = Broadcast.objects.filter(receiver = user,message_status='UNREAD')
        return {
            'PROCESS': len(objs.filter(broadcast_type = '1')),
            'MESSAGES': len(objs.filter(broadcast_type = '2')),
            'NOTIFICATIONS': len(objs.filter(broadcast_type = '3')) 
        }

    def getAllNotifications(self, user):
        output = []
        objs = Broadcast.objects.filter(receiver = user).exclude(message_status='DELETED').values()
        objs = objs.order_by('-message_dttm')
        for obj in objs:
            temp = {}
            for k, v in obj.items():
                if isinstance(v, datetime):
                    temp.update({k:str(v)})
                else:
                    temp.update({k:v})
            output.append(temp)
        return output
    
    def getProcessNotifications(self, user):
        output = []
        objs = Broadcast.objects.filter(receiver = user, broadcast_type = '1').exclude(message_status='DELETED').values()
        objs = objs.order_by('-message_dttm')
        for obj in objs:
            temp = {}
            for k, v in obj.items():
                if isinstance(v, datetime):
                    temp.update({k:str(v)})
                else:
                    temp.update({k:v})
            output.append(temp)
        return output


    def getMessageNotifications(self, user):
        output = []
        objs = Broadcast.objects.filter(receiver = user, broadcast_type = '2').exclude(message_status='DELETED').values()
        objs = objs.order_by('message_dttm')
        objs = objs.reverse()
        for obj in objs:
            temp = {}
            for k, v in obj.items():
                if isinstance(v, datetime):
                    temp.update({k:str(v)})
                else:
                    temp.update({k:v})
            output.append(temp)
        return output


    def getSentProcessNotifications(self, user):
        objs = Broadcast.objects.filter(sender = user, broadcast_type = '1').values()
        return objs

    def getSentMessageNotifications(self, user):
        objs = Broadcast.objects.filter(sender = user, broadcast_type = '2').values()
        return objs

    def getAllSentNotifications(self, user):
        objs = Broadcast.objects.filter(sender = user).values()
        return objs

    def setReadStatus(self, pk):
        assert(pk is not None and pk != ""), "Please specify the pk"
        try:
            obj = Broadcast.objects.get(pk = pk)
        except Broadcast.ObjectDoesNotExist:
            return "Broadcast track does not exists with the specified pk '%s'"%(str(pk))

    def setUnReadStatus(self, pk):
        try:
            obj = Broadcast.objects.get(pk = pk)
            obj.message_status = "READ"
            obj.save()
        except Broadcast.ObjectDoesNotExist:
            return "Broadcast track does not exists with the specified pk '%s'"%(str(pk))

    def setDeleteStatus(self, pk):
        try:
            obj = Broadcast.objects.get(pk = pk)
            obj.message_status = "DELETE"
            obj.save()
        except Broadcast.ObjectDoesNotExist:
            return "Broadcast track does not exists with the specified pk '%s'"%(str(pk))

    def From(self, sender):
        # rdb.set_trace()
        
        assert(sender != ""), "Sender should not be empty"
        self.sender = sender
        return self

    def To(self, receiver):
        # rdb.set_trace()

        assert(receiver != ""), "Receiver should not be empty"
        self.receiver = receiver
        return self

    def Subject(self, subject):
        # rdb.set_trace()

        assert(subject != ""), "Subject should not be empty"
        self.message_hdr = subject
        return self

    def Body(self, body):
        # rdb.set_trace()

        assert(body != ""), "Body should not be empty"
        self.message_dtl = body
        return self

    def Data(self, context):
        # rdb.set_trace()
        self.message_data = context
        return self
    
    def notify(self, **data):
        return self
    
    @property
    def as_dict(self):
        return {
            'sender':self.sender,
            'receiver':self.receiver,
            'message_hdr':self.message_hdr,
            'message_dtl':self.message_dtl,
            'message_data':getattr(self, 'message_data', ''),
            'process_id':self.process_id,
            'request_id':self.request_id,
            'message_dttm':datetime.now()
        }

class ProcessNotifier(Notifier):
    """ Process Related Notification Mechanism """

    def __init__(self, process_id, request_id):
        """ Will instantiate a Notifier object with process_id, request_id """
        assert(process_id is not None), "process_id should not be None"
        assert(request_id is not None), "request_id should not be None"
        self.process_id = process_id
        self.request_id = request_id

    def _validate(self):
        def wrapper(self):
            assert(self.sender is not None), "From should not be empty"
            assert(self.receiver is not None), "To should not be empty"
            assert(self.message_hdr is not None), "Subject should not be empty"
            assert(self.message_dtl is not None), "Body should not be empty"
        return wrapper

    def sendNoty(self, Obj):
        import json
        import requests
        try:
            dttm = Obj.success_at.__str__()
        except:
            dttm = datetime.now().__str__()
        payload =  {
            'user': Obj.receiver, 
            'count':10, 
            'data':json.dumps({
                "title":Obj.message_hdr,
                "subject":Obj.message_dtl,
                "status":Obj.exec_status,
                "process_id":Obj.process_id,
                "request_id":Obj.request_id,
                "message_status":Obj.message_status,
                "audit_dttm":dttm,
                "audit_user":Obj.sender,
                "body":Obj.message_data,
                "broadcast_id":Obj.broadcast_id
            })
        }
        status = Obj.message_status.lower() 
        sendnoty = requests.post(settings.TORNADO_URL + "/process/"+status+"/", data = payload)
        return self

    def Success(self):
        print self.as_dict
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "SUCCESS"
        Obj.success_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)
        return self
    
    def Error(self):
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "ERROR"
        Obj.error_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)        
        return self

    def Failure(self):
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "FAILURE"
        Obj.error_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)        
        return self

    def Warning(self):
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "WARNING"
        Obj.warning_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)        
        return self
    
    def Terminated(self):
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "TERMINATED"
        Obj.terminated_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)        
        return self

    def Running(self):
        print "IN RUNNING"
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "RUNNING"
        Obj.running_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)        
        return self
    
    def Queued(self):
        print "IN QUEUED"
        Obj = self.get_or_create(self.as_dict)
        Obj.exec_status = "QUEUED"
        Obj.queued_at = datetime.now()
        Obj.save()
        self.sendNoty(Obj)
        return self


class MessageNotifier(Notifier):

    def __init__(self):
        # assert(process_id is not None), "process_id should not be empty"
        # assert(request_id is not None), "request_id should not empty"
        # self.process_id = process_id
        # self.request_id = request_id
        super(MessageNotifier, self).__init__()
    
    def _validate(self):
        def wrapper(self):
            assert(self.sender is not None), "From should not be empty"
            assert(self.receiver is not None), "To should not be empty"
            assert(self.message_hdr is not None), "Subject should not be empty"
            assert(self.message_dtl is not None), "Body should not be empty"
        return wrapper

    def sendNoty(self, Obj):
        import json
        import requests
        try:
            dttm = Obj.success_at.__str__()
        except:
            dttm = datetime.now().__str__()
        payload =  {
            'user': Obj.receiver, 
            'count':10, 
            'data':json.dumps({
                "title":Obj.message_hdr,
                "subject":Obj.message_dtl,
                "status":Obj.exec_status,
                "message_status":Obj.message_status,
                "audit_dttm":dttm,
                "audit_user":Obj.sender,
                "body":Obj.message_data,
                "broadcast_id":Obj.broadcast_id 
            })
        }
        status = Obj.message_status.lower() 
        sendnoty = requests.post(settings.TORNADO_URL + "/message/"+status+"/", data = payload)
        return self



class ProcessNotificationManager(View):
    def get(self, request):
        if(('start_records' in request.GET and request.GET['start_records'] != "") and ('end_records' in request.GET and request.GET['end_records'] != "") ):
            user = request.user
            notifier = Notifier()
            count = notifier.getNotificationCount(user)
            data = notifier.getProcessNotifications(user)
            records_count = len(data)
            data = data[int(request.GET['start_records']):int(request.GET['end_records'])]
            return HttpResponse(json.dumps({'count':count, 'data':data,'records_count':records_count}))
        else:
            return HttpResponse('No records')


    def post(self, request):
        assert(request.body is not None), "Invalid Request"
        data = json.loads(request.body)
        if 'obj' in data and data['obj'] != '':
            broadcast_data = data['obj']
            action_instance = Broadcast.objects.get(broadcast_id=broadcast_data['broadcast_id'])
            if 'method' in data and data['method'] != '':
                if data['method'] == 'DELETED':
                    action_instance.message_status = data['method']
                    action_instance.save()

                elif data['method'] == 'UNREAD':
                    action_instance.message_status = data['method']
                    action_instance.save()

                elif data['method'] == 'READ':
                    action_instance.message_status = data['method']    
                    action_instance.save()

                sendpayload = ProcessNotifier(action_instance.process_id,action_instance.request_id)
                sendpayload.sendNoty(action_instance)
                return HttpResponse("OK")
            else:
                return HttpResponse('Invalid Method')    
        else:
            return HttpResponse('Invalid Request')        

class MessageNotificationManager(View):
                 
    def get(self, request):
        if(('start_records' in request.GET and request.GET['start_records'] != "") and ('end_records' in request.GET and request.GET['end_records'] != "") ):
            user = request.user
            notifier = Notifier()
            count = notifier.getNotificationCount(user)
            data = notifier.getMessageNotifications(user)
            message_records_count = len(data)
            data = data[int(request.GET['start_records']):int(request.GET['end_records'])]
            return HttpResponse(json.dumps({'count':count, 'data':data,'message_records_count':message_records_count}))
        else:
            return HttpResponse('No records')    

    def post(self, request):
        assert(request.body is not None), "Invalid Request"
        data = json.loads(request.body)
        if 'obj' in data and data['obj'] != '':
            broadcast_data = data['obj']
            action_instance = Broadcast.objects.get(broadcast_id=broadcast_data['broadcast_id'])
            if 'method' in data and data['method'] != '':
                if data['method'] == 'DELETED':
                    action_instance.message_status = data['method']
                    action_instance.save()

                elif data['method'] == 'UNREAD':
                    action_instance.message_status = data['method']
                    action_instance.save()

                elif data['method'] == 'READ':
                    action_instance.message_status = data['method']    
                    action_instance.save()

                sendpayload = MessageNotifier()
                sendpayload.sendNoty(action_instance)
                return HttpResponse("OK")
            else:
                return HttpResponse('Invalid Method')    
        else:
            return HttpResponse('Invalid Request')        



class PreferencesWrapper(object):

    def __init__(self, *args, **kwargs):
        pass

    def updatePreferences(self, name=None, data=None):
        try:
            prefObj = UserPreferences.objects.get(username = name)
        except UserPreferences.DoesNotExist:
            return False
        prefObj.data = data
        prefObj.save()
        return True

    def updateThemePreferences(self, username=None, theme='Watermelon'):
        try:
            prefObj = UserPreferences.objects.get(username = username)
        except UserPreferences.DoesNotExist:
            return False
        data = prefObj.data
        data.update({'theme':theme}) 
        prefObj.data = data
        prefObj.save()
        return True

    def getPreferences(self, username=None):
        try:
            prefObj = UserPreferences.objects.get(username = username)
        except UserPreferences.DoesNotExist:
            return False
        return prefObj.data

    def createPreference(self, name=None, data=None):
        prefObj = UserPreferences()
        prefObj.name = name
        prefObj.data = data
        prefObj.save()
        return True


class ThemeManager(object):

    def __init__(self, *args, **kwargs):
        pass

    def _uploadTheme(self, name=None, data=None):
        pass

    def addTheme(self, name=None, data=None):
        themObj = UserTheme()
        themObj.name = name
        themObj.data = data
        themObj.save()
        return True

    def getAllThemes(self):
        from django.core import serializers
        from django.http import JsonResponse
        themes = UserTheme.objects.all()
        return JsonResponse(serializers.serialize('json', themes), safe=False)

def get_themes(request):
    thmMgr = ThemeManager()
    return thmMgr.getAllThemes()

def get_user_preferences(request):
    prefWrapper = PreferencesWrapper()
    return HttpResponse(json.dumps({'theme':prefWrapper.getPreferences(username = request.user.username)}))
    

def updateThemePreferences(request):
    theme = request.GET['theme']
    prefWrapper = PreferencesWrapper()
    prefWrapper.updateThemePreferences(username = request.user.username, theme = theme)
    return HttpResponse("Ok")


#Usage
""""
proces = ProcessNotifier("process_id", "request_id")
    .From("partha")
    .To(["Saradhi"])
    .Subject("FTP SYNC")
    .Body("aasdfasdf")
    .Data({})
    .Queued()
"""

"""
msg = MessageNotifier("process_id")
    .From("partha")
    .To(["saradhi"])
    .Subject("Hi")
    .Body("body")
    .send()
"""

""" 
Creating Customer Notifier 


from sunrise.contrib.notifications.views import Notifier

class CustomNotifier(Notifier):

    @_validate
    def custom_method(self):
        ''' you can access all information here '''
        #self.sender,self.receiver 
        pass
"""
