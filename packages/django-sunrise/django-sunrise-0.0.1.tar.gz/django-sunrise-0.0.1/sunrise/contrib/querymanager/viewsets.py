# Author: Integra
# Dev: Partha
import json, pandas as pd

from django.apps import apps
from django.db import connection
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sunrise.restful.viewsets import ViewSetManager as SunriseModelViewSet
from sunrise.restful.viewsets import MultiResourceAPIView
from sunrise.contrib.jobs.models import ReqHeader

from .models import QueryManager
from .models import RequestQueryViewer
from .serializers import QueryManagerSerializer
from .serializers import RequestQueryViewerSerializer


PAGE_MODElS = {
       'PROCESS BILLING': {
            'Process Billing': ['ProcessBillHeader','CounterpartyVerification','ProcessBillInvestor','ImportTargetReports','ImportTargetUpload','DataIntegrityChecks','ProcessBills','VerifyInvestorAttachments','VerifyLoanAttachments','DataIntegrityAttachments'],
            'Review Pricing Models': ['ReviewBillsHdr', 'ReviewBillsDtl']
        },
        'SETUP BILLING': {
            'Define Billing Categories': ['BillingCategory'],
            'Define Billing Events': ['BillingEventHdr', 'BillingEventDtl'],
            'Define Billling Templates': ['BillingTemplateHdr', 'BillingTemplateDtl'],
            'Define Pricing Models': ['PricingModelHdr','PricingModelDtl','PricingMarkupDtl','PricingDataIntegrity','PricingEventMeasDtl','PricingTierDtl'],
            'Import Format Designer': ['ImportFormatDesigner','ImportFormatDesignerDtl'],
            'Source Tables': ['UnremiLoss','BoardingFees']
        },
        'SETUP COUNTERPARTIES': {
            'Define Bills': ['DefineBills','InvestorReference','BillAttachments','VerifyBill','BillDataImports','BillDataIntegrity'],
            'Define Counter Parties': ['DefineCounterparties', 'BillReference'],
            'Define Investors': ['DefineInvestor', 'InvestorLoans']
        },
        'DASHBOARD':{
            'Dashboard':['DashboardDummyData']
        },
    }

class QueryManagerViewSet(SunriseModelViewSet):
    model = QueryManager
    parser = {
        'default': QueryManagerSerializer,
    }

class ModelRecords(APIView):
    """
    Used to return the page related models
    """
    def get(self, request, format=None):
        META_COLS = ['blank', 'null', 'help_text', 'max_length', 'choices']
        custom_labels = []
        model_records, model_relations = {}, {}
        for model in apps.get_models()[6:]:
            modelname = model._meta.object_name
            if modelname != 'AccessToken':
                fields, help_texts, relations, data_types = [], [], [], []
                fkey = {}
                for field in model._meta.fields:
                    field_name=field.name
                    if modelname in ['User']:
                        htext = 'ID' if field.name=='id' else field.name.title().replace('_',' ')               
                    else:
                        htext = field.help_text if field.name not in custom_labels else custom_labels[field.name]
                        htext = field.name.title().replace('_',' ') if htext == '' else htext
                        htext = 'ID' if htext == 'Id' else htext
                    if field.get_internal_type() == "ForeignKey":
                        field_name = field.name+"_id"
                        fkey[field_name] = htext
                        relations.append(field.rel.to.__name__)  
                    if field.get_internal_type() == "JSONField":
                        # For JSONField you can access the data using '->(index:int), ->>(key:text), #>(nested), #>>(nested, key)
                        # Here we're assuming everything is just key:val
                        _qset = model.objects.all()[:1].values_list(field_name, flat = True)
                        if len(_qset) > 0:
                            try:
                                _in_keys = _qset[0].keys()
                                for _key in _in_keys:
                                    _field_name = field_name
                                    _field_name = _field_name + "->>'" + _key +"'"
                                    fields.append(_field_name)  
                                    help_texts.append(_key)  
                                    _temp = { item: field.__dict__.get(item, '') for item in META_COLS}
                                    try:
                                        _temp.update({'type':field.get_internal_type()})
                                    except:
                                        pass
                                    data_types.append(_temp)                    
                            except:
                                pass
                    if field.get_internal_type() != "JSONField":
                        help_texts.append(htext)
                        fields.append(field_name)
                        _temp = { item: field.__dict__.get(item, '') for item in META_COLS}
                        try:
                            _temp.update({'type':field.get_internal_type()})
                        except:
                            pass
                        data_types.append(_temp)                                    
                cfields = {fields[i]:help_texts[i] for i in range(len(fields))}
                field_data_types = {fields[i]:data_types[i] for i in range(len(fields))}

                model_records[modelname]={'fields':cfields,'_meta': field_data_types,'parents':relations,'db_model':model._meta.db_table,'pkey':model._meta.pk.name,'fkey':fkey}
        return HttpResponse(json.dumps({'models':PAGE_MODElS,'records':model_records}) )

    def post(self, request):
        return Response({"message": "Not Implemented"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)        

class DashBoardResults(APIView):

    def get(self, request):
        return Response({"message": "Not Implemented"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        if 'query' in request.POST:
            query = request.POST['query']
        if 'fields' in request.POST:
            for_fields = json.loads(request.POST['fields'])
        if 'source_query' in request.POST:
            queryset = QueryManager.objects.filter(name = request.POST['source_query'])
            if queryset.count() == 0 :
                return HttpResponse('Query not found', status=404)
            else:
                availablefields = []
                query = queryset[0].summary
                for record in queryset[0].records:
                    for field in record['fields']:
                        if field.get('select', False) == True:
                            availablefields.append(field['field_text'])
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        fields = [ field.name for field in cursor.description]

        dashboard = pd.DataFrame.from_records(data, columns=fields)
        
        dashboard = dashboard[for_fields]
        dashboard[for_fields[1:]] = dashboard[for_fields[1:]].astype(float)
        dashboard = dashboard.to_records(index=False).tolist()

        dashboard.insert(0, for_fields)
        if 'source_query' in request.POST:
            return HttpResponse(json.dumps({'result': dashboard, 'fields': availablefields}, default=str))
        try:
            data = json.dumps({'result': dashboard})
        except: 
            data = json.dumps({'result': dashboard}, default=str)

        return HttpResponse(json.dumps({'result': dashboard}, default=str))

class QueryResults(MultiResourceAPIView):

    def getData(self, request, *args, **kwargs):
        INPUT = request.GET
        query = INPUT['query']
        cursor = connection.cursor()
        cursor.execute(query+";")
        data=cursor.fetchall()
        fields = [ field.name for field in cursor.description ]
        return {
            'data':data,
            'fields': fields
        }

class RequestQueryViewerViewSet(SunriseModelViewSet):
	model = RequestQueryViewer
	parent = ReqHeader

	parser = {
		'default': RequestQueryViewerSerializer
	}