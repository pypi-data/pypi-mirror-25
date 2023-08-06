# Author: Integra
# Dev: Partha(Ref), Krishna(Ref)

import json, pytz
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from sunrise.restful.viewsets import ViewSetManager as SunriseModelViewSet

from .serializers import CustomerSerializer,SunriseProfileSerializer,SunriseProfileCreateSerializer, PageGroupSerializer,SunriseRoleSerializer,RolePageAccessSerializer,SunriseProfileRolesAssignedSerializer, UserListSerializer, SunriseProfileRetrieveSerializer,UserSerializer, RolePageListAccessSerializer, SunriseProfileRolesAssignedListSerializer, SearchCriteriaSerializer
from .models import Customer, SunriseProfile, PageGroup, SunriseRole, RolePageAccess, SunriseProfileRolesAssigned, SearchCriteria
from .handlers import send_mail, default_token_generator


class CustomerViewSet(SunriseModelViewSet):
    model = Customer
    parser = {
        'default': CustomerSerializer,
    }
    def post_save(self, request, instance, created, data):
        customer = Customer.objects.all()[0]
        profiles = SunriseProfile.objects.all()
        if ('pwd_expire_period_state' in data.keys() and data['pwd_expire_period_state'] == True) or ('pwd_expire_period' in data.keys()):
            if customer.pwd_expire_period_state == True and customer.pwd_expire_period != '':
                for profile in profiles:
                    profile.pwd_expire_from = datetime.now()
                    profile.pwd_expire_to = datetime.now() + timedelta(days = int(customer.pwd_expire_period))
                    profile.save()
            else:
                for profile in profiles:
                    profile.pwd_expire_from = None
                    profile.pwd_expire_to = None
                    profile.save()
        return instance
    

class UserViewset(SunriseModelViewSet):
    model = User
    parser = {
        'default':UserSerializer,
        'list':UserListSerializer
    }

class SunriseProfileViewSet(SunriseModelViewSet):
    model = SunriseProfile
    parser = {
        'default': SunriseProfileRetrieveSerializer,
        'list':SunriseProfileSerializer,
        'create': SunriseProfileCreateSerializer,
        'retrieve': SunriseProfileRetrieveSerializer,
        'update': SunriseProfileCreateSerializer
    }

    def populate(self, request, context, mode):
        if 'password' in context.keys():
            context.update({'password': make_password(context['password']) })
        return context
    def post_save(self, request, instance, created, data):
        user = instance
        customer_data = Customer.objects.all()
        if user.pwd_expire_from == None or user.pwd_expire_to == None:
            user.pwd_expire_from = datetime.now()
            if customer_data[0].pwd_expire_period not in [None,'']:
                user.pwd_expire_to = datetime.now() + timedelta(days = int(customer_data[0].pwd_expire_period))
        if 'lockout_account' in request.POST and request.POST['lockout_account']=='off':
            user.login_attempts=0
        user.save()
        if created:
            email1 = [user.email]
            msg = {}
            context = {'user': user, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunriserecon.com' ,'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user), 'protocol': 'http', 'mfa_enabled':customer_data[0].enable_mfa }
            msg['email_list'] = email1
            msg['user_id'] = user.username
            msg['subject'] = " Create Password in " + request.META['HTTP_HOST']
            from django.template.loader import get_template
            msg['body'] = get_template('email_templates/set_password.html').render(context)
            send_mail(**msg)
        return instance    

class PageGroupViewSet(SunriseModelViewSet):
    model = PageGroup

    parser = {
        'default': PageGroupSerializer,
    }

    # def populate(self, request, context, mode):
    #     cstObj = Customer.objects.all()[0]
    #     context.update({'customer_id': cstObj.pk })
    #     return context


class SunriseRoleViewSet(SunriseModelViewSet):
    model = SunriseRole
    parser = {
        'default': SunriseRoleSerializer,
    }

class RolePageAccessViewSet(SunriseModelViewSet):
    model = RolePageAccess
    parent = SunriseRole
    parser = {
        'default': RolePageAccessSerializer,
        'list':RolePageListAccessSerializer
    }

    def populate(self, request, context, mode):
        if context is not None:
            try:
                if 'page_id' in context.keys():
                    context['page'] = context['page_id']
                if 'page' in context.keys() and 'page_id' not in context.keys():
                    obj = PageGroup.objects.get(page = context['page'])
                    context['page'] = obj.pk
                    context['page_id'] = obj.pk
                if 'role' in context.keys():
                    context['role_id'] = context['role']
                elif 'role_id' in context.keys():
                    context['role'] = context['role_id']
            except:
                pass
        context.update({'is_active':True})
        return context



class SunriseProfileRolesAssignedViewSet(SunriseModelViewSet):
    model = SunriseProfileRolesAssigned
    parent = SunriseProfile
    parser = {
        'default': SunriseProfileRolesAssignedSerializer,
        'list':SunriseProfileRolesAssignedListSerializer
    }

    def populate(self, request, context, mode):
        try:
            if 'role_nm' in context.keys():
                rol = SunriseRole.objects.get(role_nm = context['role_nm'])
                context.update({'role': int(rol.pk)})
                context.update({'role_id': int(rol.pk)})
        except:
            pass
        try:
            if 'role' in context.keys():
                context['role_id'] = int(context['role'])
            elif 'role_id' in context.keys():
                context['role'] = int(context['role_id'])
        except:
            pass
        return context    


class SearchCriteria(SunriseModelViewSet):
    model = SearchCriteria
    parser = {
        'default': SearchCriteriaSerializer,
    }

    def populate(self, request, context, mode):
        context.update({'created_by': request.user.username })
        return context
