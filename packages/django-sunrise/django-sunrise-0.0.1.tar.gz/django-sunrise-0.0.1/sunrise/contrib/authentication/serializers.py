# Author: Integra
# Dev: Partha(Ref)

from django.contrib.auth.models import User

from rest_framework import serializers as baseserializer
from rest_framework_hstore.fields import HStoreField

from sunrise.restful import serializers
from sunrise.restful.serializers import NormalSerializer, GridSerializer

from .models import Customer, SunriseProfile, PageGroup, SunriseRole, RolePageAccess, SunriseProfileRolesAssigned, SearchCriteria

class UserListSerializer(GridSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'grid_index')

class UserSerializer(NormalSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

class CustomerSerializer(NormalSerializer):
    class Meta:
        model = Customer

class SunriseProfileSerializer(NormalSerializer):
    class Meta:
        model = SunriseProfile
        fields = ("id", "description","login_via","lockout_account","rec_sys_not","title","enable_trace_opt","pwd_hint", "username", "first_name", "last_name","is_superuser", "is_staff","email","data", "password_expired")

class SunriseProfileRetrieveSerializer(NormalSerializer):
    data = HStoreField()
    class Meta:
        model = SunriseProfile
        fields = ("id", "username", "first_name", "last_name", "password", "is_superuser", "is_staff","description","login_via","lockout_account","rec_sys_not","title","enable_trace_opt","pwd_hint", "roles", "data", "email", "password_expired")

class SunriseProfileCreateSerializer(NormalSerializer):
    data = HStoreField()
    class Meta:
        model = SunriseProfile
        fields = ("username", "first_name", "last_name", "is_staff", "is_superuser","description","login_via","lockout_account","rec_sys_not","title","enable_trace_opt","pwd_hint", "roles", "data", "email", "password_expired")

class PageGroupSerializer(NormalSerializer):
    class Meta:
        model = PageGroup

class SunriseRoleSerializer(NormalSerializer):
    class Meta:
        model = SunriseRole
        fields = ('id', 'role_nm','description', 'status', 'is_support_admin', 'audit_name', 'audit_dttm')

class RolePageListAccessSerializer(GridSerializer):
    page = baseserializer.SerializerMethodField('get_roleObj')
    description = baseserializer.SerializerMethodField('getDescription')
    def get_roleObj(self, obj):
        page_id = self.getAttr(obj, 'page_id')
        try:
            val = PageGroup.objects.get(pk = page_id)
            return val.page
        except:
            return ""
    def getDescription(self, obj):
        page_id = self.getAttr(obj, 'page_id')
        try:
            val = PageGroup.objects.get(pk = page_id)
            return val.short_description
        except:
            return ""
    class Meta:
        model = RolePageAccess
        fields = ('id', 'page', 'description', 'access_type', 'grid_index')

class RolePageAccessSerializer(GridSerializer):
    class Meta:
        model = RolePageAccess

class SunriseProfileRolesAssignedSerializer(NormalSerializer):
    profile_id = baseserializer.SerializerMethodField()
    role_id = baseserializer.SerializerMethodField()
    def get_profile_id(self, obj):
        try:
            return int(obj.profile_id)
        except:
            return int(obj['profile_id'])
    def get_role_id(self, obj):
        try:
            return int(obj.role_id)
        except:
            return int(obj['role_id'])
    class Meta:
        model = SunriseProfileRolesAssigned

class SunriseProfileRolesAssignedListSerializer(GridSerializer):
    role_nm = baseserializer.SerializerMethodField('get_roleObj')
    description = baseserializer.SerializerMethodField('getDescription')

    def _getRoleObj(self, pk):
        self.roleObj = SunriseRole.objects.get(pk = pk)

    def get_roleObj(self, obj):
        role_id = self.getAttr(obj, 'role_id')
        try:
            val = SunriseRole.objects.get(pk = role_id)
            return val.role_nm
        except:
            return ""

    def getDescription(self, obj):
        role_id = self.getAttr(obj, 'role_id')
        try:
            val = SunriseRole.objects.get(pk = role_id)
            return val.description
        except:
            return ""

    class Meta:
        model = SunriseProfileRolesAssigned
        fields = ("id", "role_nm", "description", 'grid_index')

class SearchCriteriaSerializer(NormalSerializer):
    data = HStoreField()
    class Meta:
        model = SearchCriteria
