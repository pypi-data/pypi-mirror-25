# Author: Integra
# Dev: Partha(Ref)

import random, string, requests, json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sunrise.pages.category import Category1
from sunrise.pages.search_add_view import SearchAddView

from .models import RequestHandshake
from .viewsets import OAuthApplicationViewset, AppResourcePermissionViewset

class OauthApplicationiView(Category1):
    parent = OAuthApplicationViewset
    childs = [(AppResourcePermissionViewset, 'grid', 'app_permissions'),]

class RequestHandshakeView(SearchAddView):
    pass

@csrf_exempt
def portal_handshake_response(request):
    output = request.POST
    reqObj = RequestHandshake.objects.get(from_origin = output['name'])
    reqObj.access_key = output['client_id']
    reqObj.secret_key = output['client_secret']
    reqObj.status = "Approved"
    reqObj.REF_CODE = output["REF_CODE"]
    reqObj.save()   
    return HttpResponse("Handshaked Successfully")   

@csrf_exempt
def request_billing_access(request):
    output = request.POST
    reqObj = RequestHandshake.objects.get(from_origin = output['origin'])
    reqObj.status = "Access Requested"
    reqObj.REF_CODE = output["REF_CODE"]
    reqObj.save()   
    return HttpResponse("Handshaked Successfully")  