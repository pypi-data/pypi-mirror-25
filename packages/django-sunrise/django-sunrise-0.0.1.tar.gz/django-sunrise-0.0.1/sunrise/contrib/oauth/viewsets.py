# Author: Integra
# Dev: Partha(Ref)

import requests, random, string, json
from oauth2_provider.models import Application 

from sunrise.restful.viewsets import ViewSetManager as SunriseModelViewSet

from .models import AppResourcePermission, RequestHandshake
from .serializers import ApplicationDefaultSerializer, ApplicationListSerializer, AppResourcePermissionDefaultSerializer, AppResourcePermissionListSerializer, RequestHandshakeSerializer


class OAuthApplicationViewset(SunriseModelViewSet):
    model = Application
    parser = {
        'default':ApplicationDefaultSerializer,
        'list': ApplicationListSerializer
    }
    def populate(self, request, context, mode):
        context.update({'user': request.user.pk})
        return context

class AppResourcePermissionViewset(SunriseModelViewSet):
    parent = Application
    model = AppResourcePermission
    parser = {
        'default': AppResourcePermissionDefaultSerializer,
        'list': AppResourcePermissionListSerializer
    }

class RequestHandshakeViewSet(SunriseModelViewSet):
    model = RequestHandshake
    parser = {
        'default': RequestHandshakeSerializer
    }

    def post_save(self, request, instance, created, data=None):
        if instance.status == "Request Portal Handshake" and data is not None:
            ap_dict = {}
            ap_dict['origin'] = instance.from_origin
            ap_dict['counterparty'] = data.get('counterparty', None)
            #2. Send to portal
            resp = requests.post(instance.url + "/api/portal_handshake_request/", ap_dict) 
            instance.status = "Request Portal Handshake Accepted"
            instance.save() 
        if instance.status == "Grant Access" and data is not None:
            #1. Create oauth application
            try:
                oap = Application.objects.get(name = instance.url)
            except:
                oap = None
                pass
            if oap is None:
                ap_dict = {}
                ap_dict['name'] = instance.url
                ap_dict['client_id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                ap_dict['client_secret'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
                ap_dict['client_type'] = 'confidential'
                ap_dict['authorization_grant_type'] = 'client-credentials'
                ap_dict['user'] = request.user
                oap, created = Application.objects.get_or_create(**ap_dict) 
                ap_dict['origin'] = instance.from_origin
                perObj = AppResourcePermission()
                #Creating Permissions
                perObj.appID = oap
                perObj.api_url = "/api/process/review_bills_hdr/"
                perObj.can_list = True
                perObj.can_retrieve = True
                perObj.save()

                perObj = AppResourcePermission()
                perObj.appID = oap
                perObj.api_url = "/api/process/review_bills_dtl/"
                perObj.can_list = True
                perObj.can_retrieve = True
                perObj.save()

                perObj = AppResourcePermission()
                perObj.appID = oap
                perObj.api_url = "/api/process/review_bills_message/"
                perObj.can_list = True
                perObj.can_retrieve = True
                perObj.can_create = True
                perObj.can_update = True                
                perObj.save()

                ap_dict['user'] = ''
                #2. Send to portal
                resp = requests.post(instance.url + "/api/grant_billing_access/", ap_dict)  
            else:
                resources = AppResourcePermission.objects.filter(appID = oap)
                for every_resource in resources:
                    every_resource.can_list = True
                    every_resource.can_retrieve = True
                    every_resource.save()
                #send status to portal
                to_send = {
                    'origin': instance.from_origin,
                    'client_id':oap.client_id,
                    'client_secret':oap.client_secret
                }
                resp = requests.post(instance.url + "/api/grant_billing_access/", to_send)  
        if instance.status == "Revoke Access" and data is not None:
            try:
                oap = Application.objects.get(name = instance.url)
                resources = AppResourcePermission.objects.filter(appID = oap)
                for every_resource in resources:
                    every_resource.can_list = False
                    every_resource.can_retrieve = False
                    every_resource.save()
                #send status to portal
                to_send = {
                    'origin': instance.from_origin,
                    'client_id':oap.client_id,
                    'client_secret':oap.client_secret
                }
                resp = requests.post(instance.url + "/api/revoke_billing_access/", to_send)
            except Application.DoesNotExists:
                pass
            
        return instance