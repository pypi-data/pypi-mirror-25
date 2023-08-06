""" Login Verification Module """
# Author: Partha

import hashlib
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


class LoginRequired(object):
    """ Used for login verfication """

    BYPASS = [
        '/o/token/',
        '/forgot_password/',
        '/password_reset_confirm/',
        '/password_preferences/',
        '/enable_mfa_initial/',
        '/api/portal_handshake_request/',
        '/api/grant_billing_access/',
        '/api/request_billing_access/',
        '/api/revoke_billing_access/',
        '/portal/send_counterparty_notification/'
    ]
    BYPASS_IF_STARTSWITH = [
        '/mfa_confirm/',
        '/password_reset_confirm/'
    ]
    def process_request(
            self,
            request
    ):
        """ request intake """
        try:
            request.session['TORNADO_URL'] = settings.TORNADO_URL
        except Exception, general_exception:
            pass
        try:
            if request.session.session_key is None:
                request.session.create()
            token_header = request.META["HTTP_AUTHORIZATION"]
            token_obj = re.search('(Bearer)(\s)(.*)', token_header)
            # import pdb;pdb.set_trace()
            token = token_obj.group(3)
            request.session['UUID'] = token
            if 'HTTP_X_GRIDKEY' in request.META:
                request.session['UUID'] = request.session['UUID'] + "_" + request.META['HTTP_X_GRIDKEY']
            hkey = hashlib.md5(request.session['UUID']).hexdigest()
            request.session['UUID_HASH'] = hkey
            if request.path in self.BYPASS:
                return
            bypass_found = False
            for item in self.BYPASS_IF_STARTSWITH:
                if request.path.startswith(item):
                    bypass_found = True
                    break
            if bypass_found:
                return
            if request.path.startswith("/api/"):
                return
            return
        except Exception, general_exception: #OnKeyError
            pass
        if request.path in self.BYPASS:
            return
        bypass_found = False
        for item in self.BYPASS_IF_STARTSWITH:
            if request.path.startswith(item):
                bypass_found = True
                break
        if bypass_found:
            return
        if request.user.is_authenticated():
            if request.path == "/accounts/login/":
                return HttpResponseRedirect("/")
            try:
                tab_key = request.META['HTTP_X_TABKEY']
                prefix = request.META['HTTP_X_PREFIX'] #or you can get it from request.path
                if request.session.session_key is None:
                    request.session.create()
                session_id = request.session.session_key
                request.session['UUID'] = session_id + "_" + tab_key + "_" + prefix
                hkey = hashlib.md5(request.session['UUID']).hexdigest()
                request.session['UUID_HASH'] = session_id + "_" + hkey
                if request.path.startswith("/api/"):
                    return
            except Exception, general_exception:
                pass
            if request.session.get('UUID_HASH', None) is None:
                request.session['UUID_HASH'] = 'test'
            return
        else:
            if request.path == "/accounts/login/":
                return
            return HttpResponseRedirect('/accounts/login/?next='+request.get_full_path()+'')

def server_error_handler(
        request,
        template_name='500.html'
):
    """ Custom error handler """
    return HttpResponse("Custom")
