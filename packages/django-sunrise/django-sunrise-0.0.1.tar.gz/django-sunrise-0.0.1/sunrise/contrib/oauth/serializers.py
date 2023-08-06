# Author: Integra
# Dev: Partha

from rest_framework import serializers as baseserializer
from rest_framework_hstore.fields import HStoreField
from oauth2_provider.models import Application

from sunrise.restful import serializers
from sunrise.restful.serializers import NormalSerializer, GridSerializer
from .models import AppResourcePermission, RequestHandshake

class ApplicationDefaultSerializer(NormalSerializer):    
    class Meta:
        model = Application

class ApplicationListSerializer(NormalSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'client_id', 'redirect_uris', 'client_type', 'authorization_grant_type', 'client_secret', 'skip_authorization')

class AppResourcePermissionDefaultSerializer(NormalSerializer):
    class Meta:
        model = AppResourcePermission
        
class AppResourcePermissionListSerializer(GridSerializer):
    class Meta:
        model = AppResourcePermission
        fields = ('api_url','can_list','can_retrieve', 'can_create', 'can_update', 'can_destroy', 'grid_index')
    
class RequestHandshakeSerializer(NormalSerializer):
    class Meta:
        model = RequestHandshake

    