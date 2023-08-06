# Author: Integra
# Dev: Partha(Ref)

import json, pytz
import urllib
import urllib2
import re
from datetime import datetime,timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.template import Context, loader, RequestContext
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from sunrise.contrib.addons.models import MenuStructure
from sunrise.pages.search_add_view import SearchAddView
from sunrise.pages.category import Category1

from .models import Customer, PageGroup, SunriseRole, SunriseProfile, RolePageAccess, SunriseProfileRolesAssigned, OldPasswords
from .viewsets import SunriseRoleViewSet, RolePageAccessViewSet, SunriseProfileViewSet, SunriseProfileRolesAssignedViewSet
from .handlers import send_mail,search, default_token_generator


class UserPage(SearchAddView):
    pass

class DefineUsers(Category1):
    parent = SunriseProfileViewSet
    childs = [
        (SunriseProfileRolesAssignedViewSet, 'grid', 'sunrise_profile_roles_assigned')
    ]

class DefineRoles(Category1):
    parent = SunriseRoleViewSet
    childs = [
        (RolePageAccessViewSet, 'grid', 'role_page_access')
    ]

class UserLogin(View):  

    def get(self, request):
        return render(request,'login.html', {})
    
    def post(self, request):
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        try:
            customer = Customer.objects.all()
            if len(customer) > 0:
                customer = customer[0]
            else:
                customer = None
            check_lock = SunriseProfile.objects.get(username=uname)
        except:
            check_lock = None
        if pwd == "":
            return render(request,'login.html', {'status':'invalid'})    
        
        if check_lock is None:
            return render(request,'login.html', {'status':'invalid'})
        else: 
            if check_lock.lockout_account:
                return render(request,'login.html', {'status':'locked'})
            if not check_lock.is_active:
                return HttpResponse('Account Has Been Disabled')              
        user=authenticate(username=uname, password=pwd)
        if user is not None:      
            if customer is not None and customer.pwd_expire_period_state == True and user.pwd_expire_to is not None and customer.pwd_expire_period != '' and customer.pwd_expire_check:
                now_datetime = pytz.utc.localize(datetime.now())
                date_diff = (user.pwd_expire_to - now_datetime).days
                if date_diff <= int(customer.pwd_expire_check):
                    if date_diff <= 0:
                        user.password_expired = True
                        user.save()
                        #Email Notification
                        msg = {}
                        context = {'user': user, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunrisebilling.com' ,'uid': urlsafe_base64_encode(force_bytes(check_lock.pk)), 'token': default_token_generator.make_token(check_lock), 'protocol': 'http',}
                        msg['email_list'] = [user.email]
                        msg['user_id'] = user.username
                        msg['subject'] = "Change Your Password in " + request.META['HTTP_HOST']
                        from django.template.loader import get_template
                        msg['body'] = get_template('email_templates/password_expired.html').render(context)
                        send_mail(**msg)
                        return render(request,'login.html', {'status':'pwdexpired'})
                    else:
                        ##Reminder Keep Global Broadcast Partha
                        msg = {}
                        from django.template.loader import get_template
                        context = {'user': user , 'expired_msg': 'Your Password will Expire in '+str(date_diff) +' days','host':request.META['HTTP_HOST']}
                        msg['email_list'] = [user.email]
                        msg['user_id'] = uname
                        msg['subject'] = "Change Your Password in " +request.META['HTTP_HOST']
                        msg['body'] = get_template('email_templates/password_expiry_notification.html').render(context)
                        send_mail(**msg)
            if user.login_attempts > 0:
                user.login_attempts = 0
                user.save()    
            request.session['customer'] = customer
            login(request, user)
            #Build accessbile urls here
            accessible_urls(request)
            if 'next' in request.GET:
                from .handlers import resolve_redirect_url
                rpath =  resolve_redirect_url(request.GET['next'])
                return HttpResponseRedirect('%s'%rpath)

            else:    
                return HttpResponseRedirect('/')    

        else:
            if customer is not None and customer.max_login_attempts_state == True:
                if int(customer.max_login_attempts)-1 > check_lock.login_attempts:
                    check_lock.login_attempts = check_lock.login_attempts + 1
                else:
                    from django.template.loader import get_template
                    from django.template import Context
                    check_lock.lockout_account = True
                    email = check_lock.email
                    msg = {}
                    context = {'user': check_lock, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunrisebilling.com' ,'uid': urlsafe_base64_encode(force_bytes(check_lock.pk)), 'token': default_token_generator.make_token(check_lock), 'protocol': 'http',}
                    msg['email_list'] = [email]
                    msg['user_id'] = check_lock.username
                    msg['subject'] = "Password Reset in " +request.META['HTTP_HOST']
                    msg['body'] = get_template('email_templates/email_lock.html').render(context)
                    send_mail(**msg)        
                check_lock.save()
            return render(request,'login.html', {'status':'invalid'})


def UserLogout(request):
    from sunrise.cache import ResourceCache
    try:
        cache_manager = ResourceCache(UUID_HASH = request.session['UUID_HASH'])
        pattern = request.session['UUID_HASH'].split("_")[0]
        cache_manager.deletePattern(pattern)
    except:
        pass
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

def build_menu(request):
    menu = []
    mobj = MenuStructure.objects.all()
    if len(mobj) > 0:
        data = json.loads(mobj[0].data['data'])[0]
    for iitem in data:
        if iitem['name'] == 'ALL':
            continue
        temp = []
        url_count = 0
        for item in iitem['values']:
            if 'is_divider' in item.keys():
                temp.append({'name':'', 'url':'', 'type':'DIVIDER'})
            elif 'is_group' in item.keys():
                temp.append({'name':item['name'], 'url':'', 'type':'GROUP'})                
            elif 'url' in item.keys() and item['url'] in request.session['accessible_urls']:
                url_count = url_count + 1
                _action = 'search'
                if item['page_category'] != '1':
                    _action = 'view'
                temp.append({'name':item['page'], 'url':item['url'], 'type':'SUBMENU', 'page_category':_action})
        if url_count > 0:
            menu.append({'name':iitem['name'].upper(), 'values':temp})
    request.session['menu'] = menu



def accessible_urls(request):
    if (request.user.username=='admin'):#admin return
        pages=PageGroup.objects.all()
        accessible_urls=[]
        for i in pages:
            accessible_urls.append(i.url)
        accessible_urls.append('/default/') # to give admin access to all defined and undefined urls
        request.session['accessible_urls']=accessible_urls
        build_menu(request)
        return
    profile=SunriseProfile.objects.get(username=request.user.username)
    roles = profile.roles.all()
    accessible_urls=[]
    for role in roles:
        pages = role.pages.all()
        for page in pages:
            accessible_urls.append(page.url)
    request.session['accessible_urls']=accessible_urls
    build_menu(request)


class PasswordPreferences(View):
    
    def getUserFromUIB(self,uidb64):
        uid = urlsafe_base64_decode(uidb64)
        user = SunriseProfile.objects.get(pk=uid)
        return user

    def logPassword(self, request, user, password):
        obj = OldPasswords.objects.create(user = user, pwds = password, audit_dttm = datetime.now(), audit_user = request.user.username)
        return obj
        

    def post(self,request):
        #validation for password'
        data = json.loads(request.body)
        user = SunriseProfile.objects.get(username = data['username'])
        pwd_preferences = Customer.objects.all()[0]
        n = pwd_preferences.min_old_passwords_remember
        try:
            _passwords = OldPasswords.objects.filter(user = user).values("pwds").order_by("-pk")[:n]
        except:
            _passwords = []    
        _found = False
        for pwd in _passwords:
            if check_password(data['new_pwd'], pwd['pwds']):
                _found = True
                break
        found, result = search(data['new_pwd'])
        return HttpResponse(json.dumps({'no_password_dictionary': found, 'no_four': _found}))    


    def get(self,request):
        pwd_perference = {}
        try:
            user = request.user
        except :
            if type(request) is User:
                user = request            
        customer_data = Customer.objects.all()
        try:
            if request.method == "GET" and 'uidb64' in request.GET.keys():
            #1. Get user here using uib
                user = self.getUserFromUIB(request.GET['uidb64'])        
        except:
            if type(request) is User:
                user = request

        try:
            pwd_perference['first_name'] = user.first_name
            pwd_perference['last_name'] = user.last_name
            pwd_perference['email'] = user.email
            pwd_perference['user_name'] = user.username
        except:
            pass
            
        pwd_perference["pwd_min_length"]=customer_data[0].pwd_min_length
        pwd_perference["upper_or_lower"]=customer_data[0].upper_or_lower
        pwd_perference["one_number"]=customer_data[0].one_number
        pwd_perference["special_character"]=customer_data[0].special_character
        pwd_perference["no_email"]=customer_data[0].no_email
        pwd_perference["no_first_or_last_name"]=customer_data[0].no_first_or_last_name
        pwd_perference["no_password_dictionary"]=customer_data[0].no_password_dictionary
        pwd_perference["no_username"]=customer_data[0].no_username
        pwd_perference["min_old_passwords_remember"]=customer_data[0].min_old_passwords_remember
        pwd_perference["min_old_passwords_remember_state"]=customer_data[0].min_old_passwords_remember_state
        if customer_data[0].pwd_expire_period:
            pwd_perference['pwd_expire_period'] = customer_data[0].pwd_expire_period
        response = dict()
        response['pwd_perference'] = pwd_perference
        try:
            if request.is_ajax:
                return HttpResponse(json.dumps(response))
            else:
                return json.dumps(response)
        except:
            return json.dumps(response)



    # validation for Passwords        
    def validate(self,request):
        data = json.loads(request.body)
        user = Users.objects.get(username = data['username'])
        pwd_preferences = PasswordPreferences.objects.all()[0]
        n = pwd_preferences.min_old_passwords_remember
        try:
            _passwords = OldPasswords.objects.filter(user = user).values("pwds").order_by("-pk")[:n]
        except:
            _passwords = []    
        _found = False
        for pwd in _passwords:
            if check_password(data['new_pwd'], pwd['pwds']):
                _found = True
                break
        found, result = search(data['new_pwd'])
        return HttpResponse(json.dumps({'no_password_dictionary': found, 'no_four': _found}))    

        
        

def changePassword(request):
    status = ""
    pwd_perference = {}
    perference_count = 0
    actual_count = 0
    no_four_pass = True
    data = json.loads(request.body)
    new_pwd = data['new_pwd']
    old_pwd = data['old_pwd']
    user = request.user
    customer_data = Customer.objects.all()
    pwd_perference["pwd_min_length"]=customer_data[0].pwd_min_length    
    if check_password(old_pwd,user.password):
        if len(new_pwd) >= int(pwd_perference["pwd_min_length"]):
            if customer_data[0].upper_or_lower == True:
                perference_count = perference_count + 1
                if re.search('[a-z]',new_pwd) and re.search('[A-Z]',new_pwd):
                    actual_count = actual_count + 1
                else:
                     return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Atleast One upper or lower case in password'
                        }), status = 500)
                    
            if customer_data[0].one_number == True:
                perference_count = perference_count + 1
                if re.search('\d+',new_pwd):
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Atleast One number in password'
                        }), status = 500)

            if customer_data[0].special_character == True:
                perference_count = perference_count + 1
                if re.search('[!,%,&,@,#,$,^,*,?,_,~]',new_pwd):
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Atleast One Special Character in password'
                        }), status = 500)

            if customer_data[0].no_email == True:
                perference_count = perference_count + 1
                if new_pwd != user.email:
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Password Should not be equal to user email'
                        }), status = 500)

            if customer_data[0].no_first_or_last_name == True:
                perference_count = perference_count + 1
                if new_pwd != user.first_name and new_pwd != user.last_name:
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Password Should not be equal to user firstname or lastname'
                        }), status = 500)

            if customer_data[0].no_password_dictionary == True:
                perference_count = perference_count + 1
                found, result = search(new_pwd)
                if found == False:
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Password Should not be a Dictionary word'
                        }), status = 500)

            if customer_data[0].no_username == True:
                perference_count = perference_count + 1
                if new_pwd != user.username:
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Password Should not be equal to username'
                        }), status = 500)
            if customer_data[0].min_old_passwords_remember_state == True:
                perference_count = perference_count + 1
                n = customer_data[0].min_old_passwords_remember
                passes = OldPasswords().checkLastFourPasswords(user,new_pwd,n)
                if passes == False:
                    actual_count = actual_count + 1
                else:
                    return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Password Should not contain in last '+str(n)+' passwords'
                        }), status = 500)    
            if perference_count == actual_count:
                user.password=make_password(new_pwd)
                obj = PasswordPreferences()
                obj.logPassword(request, user, user.password)
                msg = {}
                email1 = user.email
                context = {'user': user,'host':request.META['HTTP_HOST']}
                msg['email_list'] = [email1]
                msg['user_id'] = user.username
                msg['subject'] = "Password Change in " + request.META['HTTP_HOST']
                from django.template.loader import get_template
                msg['body'] = get_template('email_templates/password_change.html').render(context)
                user.pwd_forgot = False
                user.password_expired = False
                if customer_data[0].pwd_expire_period_state == True:
                    user.pwd_expire_from = datetime.now()
                    user.pwd_expire_to = datetime.now() + timedelta(days = int(customer_data[0].pwd_expire_period))
                user.save()
                send_mail(**msg)
                return HttpResponse(json.dumps({
                        'type': 'success',
                        'message': 'Password Changed Successfully'
                    }))
        else:
            l=pwd_perference["pwd_min_length"]
            return HttpResponse(json.dumps({
                'type': 'error',
                'message': 'Length of password should be greater than ' +str(l)
            }), status = 500)
    else:
        return HttpResponse(json.dumps({
            'type': 'error',
            'message': 'Entered Old Password is incorrect'
        }), status = 500)



class ForgotPassword(View):
    
    def get(self,request):
        return render(request,'forgot_password.html')

    def _CheckCredentials(self, *args):
        email = args[1]
        uname = args[0]
        if email == "" and uname == "":
            return 'null'
        try:
            user = SunriseProfile.objects.get(username__iexact = uname, email__iexact = email)
            email = user.email
            return user
        except:
            return 'norecord'

    def _CheckCaptcha(self, **values):
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        return result["success"]

    def post(self,request):
        email = request.POST['email']
        uname= request.POST['username']
        user = self._CheckCredentials(uname, email)
        if user == "null":
            return render(request,'forgot_password.html', {'status':'null'})
        elif user == "norecord":
            return render(request,'forgot_password.html', {'status':'invaliduser'})
        if user.is_active:
            values = {
            'secret': settings.NORECAPTCHA_SECRET_KEY,
            'response': request.POST.get(u'g-recaptcha-response', None),
            'remoteip': request.META.get("REMOTE_ADDR", None),
            }       
            flag_proceed = self._CheckCaptcha(**values)
            if not flag_proceed:
                return render(request,'forgot_password.html', {'status':'invalidcaptcha'})
            try:
                msg = {}
                context = {'user': user, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunriserecon.com' ,'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user), 'protocol': 'http','cloud':'/cloud/'}
                msg['email_list'] = [email]
                msg['user_id'] = user.username
                msg['subject'] = "Password Reset in " +request.META['HTTP_HOST'] 
                from django.template.loader import get_template
                msg['body'] = get_template('email_templates/reset_password_email_link.html').render(context)
                send_mail(**msg)
                return render(request,'forgot_password.html', {'status':'success'})
            except Exception,e:
                print e
                return render(request,'forgot_password.html', {'status':'issueemail'})
        else:
            return HttpResponse('Inactive User')        



class PasswordResetConfirm(View):
    def get(self, request,uidb64=None, token=None, *arg, **kwargs):
        assert uidb64 is not None and token is not None, "Invalid Token"
        obj = PasswordPreferences()
        user = obj.getUserFromUIB(uidb64)
        pwd_preferences = Customer.objects.all()[0]
        token_checker, check_message = default_token_generator.check_token(user, token)
        if token_checker:
            if user.is_active:
                return render(request, 'reset_password.html',{"pwd_preferences":pwd_preferences,"user":user})
            else:
                return HttpResponse('Inactive Account Contact Administrator')      
        else:
            return HttpResponse(check_message)
    def post(self, request, uidb64=None, token=None, *arg, **kwargs):  
        data = json.loads(request.body)
        uidb64 = data['uidb64']
        token = data['token']
        try:
            obj = PasswordPreferences()
            user = obj.getUserFromUIB(uidb64)
        except Exception,e:
            print e
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            password1 = data['new_pwd']
            user.password=make_password(password1)
            obj.logPassword(request, user, user.password)
            if user.lockout_account:
                user.lockout_account = False
                user.login_attempts = 0
            user.password_expired = False
            customer = Customer.objects.all()
            if customer[0].pwd_expire_period_state == True:
                user.pwd_expire_from = datetime.now()
                user.pwd_expire_to = datetime.now() + timedelta(days = int(customer[0].pwd_expire_period))

            user.save()
            msg = {}                    
            email1 = user.email
            context = {'user': user,'host':request.META['HTTP_HOST']}
            msg['email_list'] = [email1]
            msg['user_id'] = user.username
            msg['subject'] = "Password Change in " + request.META['HTTP_HOST']
            from django.template.loader import get_template
            msg['body'] = get_template('email_templates/password_change.html').render(context)
            send_mail(**msg)
            return HttpResponse(json.dumps({
                            'type': 'success',
                            'message': 'Password Has Been Successfully Reset'
                        }))
        else:
            return HttpResponse(json.dumps({
                            'type': 'error',
                            'message': 'Invalid Token'
                        }))

def SendEmail(request):
    data = json.loads(request.body)
    customer = Customer.objects.all()[0]
    try:
        user = SunriseProfile.objects.get(username= data['username'],email= data['email'])
    except:
        return HttpResponse(json.dumps({
                'type': 'error',
                'message': 'There might be some unsaved changes.'
            }), status = 500)
    if data["id"] == "email":
        msg = {}
        context = {'user': user, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunriserecon.com' ,'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user), 'protocol': 'http','mfa_enabled': customer.enable_mfa }
        msg['email_list'] = [user.email]
        msg['user_id'] = user.username
        msg['subject'] = "Password Reset in " +request.META['HTTP_HOST'] 
        from django.template.loader import get_template
        msg['body'] = get_template('email_templates/reset_password_email_link.html').render(context)
        send_mail(**msg)
        return HttpResponse(json.dumps({
            'type': 'success',
            'message': 'Password Reset Link Sent to user Email'
        }))
    elif data['id'] == "mfa":
        msg = {}
        context = {'user': user, 'domain': request.META['HTTP_HOST'], 'site_name': 'sunriserecon.com' ,'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user), 'protocol': 'http','mfa_enabled': customer.enable_mfa}
        msg['email_list'] = [user.email]
        msg['user_id'] = user.username
        msg['subject'] = "MFA Reset in " +request.META['HTTP_HOST'] 
        from django.template.loader import get_template
        msg['body'] = get_template('email_templates/reset_password_email_link.html').render(context)
        send_mail(**msg)
        return HttpResponse(json.dumps({
            'type': 'success',
            'message': 'MFA Link Sent to user Email'
        }))        




