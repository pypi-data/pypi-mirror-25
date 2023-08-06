import os
import pytz
import re
from datetime import date,datetime
from wordnik import *

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

from sunrise.contrib.authentication.models import PageGroup

def send_mail(**kwargs):
    if 'attachment' in kwargs:
        file_name=kwargs['attachment']
    else:
        file_name=False
    from_email = settings.EMAIL_HOST_USER
    email_list = kwargs['email_list']
    subject = kwargs['subject']
    message = kwargs['body']
    msg = EmailMessage(subject=subject,to=email_list)
    msg.template_name = 'billing_template'
    msg.use_template_subject = False
    msg.use_template_from = True
    msg.global_merge_vars = { 
        'content' : message,
    }
    if file_name:
        msg.attach_file(file_name)
    msg.send()        
    if file_name and os.path.isfile(file_name):
        os.system("rm "+file_name)

def resolve_redirect_url(path):
    parts = path.split('/')
    if len(parts) > 3:
        _2nd_category_pages = list(PageGroup.objects.all().exclude(page_category = 1).values_list('url'))
        check_url = ( "/" + parts[1] + "/" + parts[2] + "/",);
        mode = parts[3]
        if (mode == 'view' or mode == 'add') and (check_url not in _2nd_category_pages):
            if mode =='add':
                path = re.sub(r"\badd\b","search",path)
            elif mode == 'view':
                path = re.sub(r"\bview\b","search",path)
    return path

    

def search(word):
    """ @param: word
        output: (found, word) """
    word = word.lower()
    found = False
    apiUrl = settings.DICT_API_URL 
    apiKey = settings.DICT_API_KEY 
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordApi.WordApi(client)
    try:
        result = wordApi.getDefinitions(word)
    except:
        result = None
    if result is not None:
        found = True
    print "result:::", result
    return (found, result)


class PasswordResetTokenGenerator(object):
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """
    def make_token(self, user):
        """
        Returns a token that can be used once to do a password reset
        for the given user.
        """
        return self._make_token_with_timestamp(user, self._num_days(self._today()))

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return (False, "Invalid Token")

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return (False, "Invalid Token")

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return (False, "Password has been already reset by the user")

        # Check the timestamp is within limit
        if ((self._num_days(self._today()) - ts)) > settings.PASSWORD_RESET_TIMEOUT_HOURS * 3600:
            return (False, "Limit Expired")

        return (True, "Success")

    def _make_token_with_timestamp(self, user, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # By hashing on the internal state of the user and using state
        # that is sure to change (the password salt will change as soon as
        # the password is set, at least for current Django auth, and
        # last_login will also change), we produce a hash that will be
        # invalid as soon as it is used.
        # We limit the hash to 20 chars to keep URL short
        key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

        # Ensure results are consistent across DB backends
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)

        value = (six.text_type(user.pk) + user.password +
                six.text_type(login_timestamp) + six.text_type(timestamp))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

    def _num_days(self, dt):
        return int((dt - datetime(2017, 1, 1)).total_seconds())

    def _today(self):
        # Used for mocking in tests
        return datetime.now()

default_token_generator = PasswordResetTokenGenerator()
