# Author: Integra
# Dev: Partha(Ref)

import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.operations import HStoreExtension
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import AbstractBaseUser, UserManager

status_type=(('Active','Active'),('Inactive','Inactive'))
type_investor=(('Gse','GSE'),('Private','PRIVATE'))
remittance_investor=(('Sch/Sch','SCH/SCH'),('Sch/Act','SCH/ACT'),('Act/Act','ACT/ACT'))
fund_type_investor=(('Saf','SAF'),('Non-Saf','NON-SAF'))
process_choices=(('1','Same as Cash Book'),('2','Following Month'))
customer_contact_type = (('',''),('Billing','Billing'),('Customer','Customer'),('Sponsor','Sponsor'),('Support','Support'),('Tech','Tech'),('User','User'))
storage_sources =(('AWS','Sunrise-Cloud'),('NAS','NAS'))
tab_setup = (('clearing','clearing'),('cashbook','cashbook'),('custodial','custodial'))
ots_process_choices = (('Accounts','Accounts'),('Investors','Investors'),('Investor Members','Investor Members'),('Loans','Loans'),('Pools','Pools'))
status = (('Active','Active'),('Inactive','Inactive'))

class Customer(models.Model):
    id = models.AutoField('ID', primary_key=True)
    customer_id = models.CharField(help_text='Customer ID', max_length = 50, unique=True)
    name = models.CharField(help_text='Name', max_length = 30,blank=True,null=True)
    status = models.CharField(help_text='Status', choices=status_type,max_length=8,default='Active')
    address_line1 = models.CharField(help_text='Address Line1', max_length = 30,blank=True,null=True)
    address_line2 = models.CharField(help_text='Address Line2', max_length = 30, blank = True)
    address_line3 = models.CharField(help_text='Address Line3', max_length = 30, blank = True)
    city     = models.CharField(help_text='City', max_length = 20,blank=True,null=True)
    state    = models.CharField(help_text='State', max_length = 2,blank=True,null=True)
    country  = models.CharField(help_text='Country', max_length = 20,blank=True,null=True)
    postal_main = models.CharField(help_text='Zip Code', max_length = 5,blank=True,null=True)
    postal_add = models.CharField(max_length = 4, blank = True,help_text='Postal Address')
    phone = models.CharField(help_text='Main Number',max_length = 15, blank = True)
    phone_ext = models.CharField(help_text='Ext',max_length = 5, blank = True)
    ##password and security perferences
    pwd_min_length = models.CharField(max_length=10,default=8,help_text='Password Length')
    upper_or_lower = models.BooleanField(default=False,help_text='Upper/Lower')
    one_number = models.BooleanField(default=False,help_text='Use Atleast Number')
    special_character = models.BooleanField(default=False,help_text='Special Character')
    no_email = models.BooleanField(default=False,help_text='No Email')
    no_first_or_last_name = models.BooleanField(default=False,help_text='No First/Last Name')
    pwd_expire_period = models.CharField(max_length = 20,blank=True,null=True,help_text='Password Expire Period')
    max_login_attempts = models.CharField(max_length = 20,blank=True,null=True,help_text='Maximum Login Attempts')
    pwd_expire_check = models.CharField(max_length = 20,blank=True,null=True,help_text='Password Expire Check')
    pwd_expire_period_state = models.BooleanField(default=False,help_text='Password Expire Period State')
    max_login_attempts_state = models.BooleanField(default=False,help_text='Max Login Attempts State')
    username_case = models.BooleanField(default=False,help_text='UserName To Upper')
    #password in dictionary and old passwords storage
    no_password_dictionary = models.BooleanField(default=False,help_text='No Password in Dictionary')
    no_username = models.BooleanField(default=False,help_text='No Username')
    min_old_passwords_remember = models.CharField(max_length=20,default=4,help_text='Number of old passwords to remember')
    min_old_passwords_remember_state = models.BooleanField(default=False,help_text='Number of old passwords to remember state')
    #SAML, MFA(Added by partha)
    enable_mfa = models.BooleanField(default = False)
    enable_saml = models.BooleanField(default = False)
    saml_url = models.CharField(max_length = 100, null = True, blank = True)
    #OTP Max Attempts
    max_otp_attempts = models.CharField(max_length = 5,default='6', blank=True,null=True,help_text='Maximum OTP Attempts')
    audit_name = models.CharField(max_length=20,blank=True,null=True,help_text='Audit Name')
    audit_dttm = models.DateTimeField(blank=True,null=True,help_text='Audit DateTime')
    #HomePage Url
    home_page_url = models.CharField(max_length = 100, null = True, blank=True)

    data = HStoreField(null = True)


    def __unicode__(self):
          return self.customer_id

    class Meta:
        db_table = 'sunrise_contrib_authentication_customer'

    def clean(self):
        if self.customer_id in [None,'']:
            raise ValidationError("Customer ID Is Required")



class PageGroup(models.Model):
    page_category_choices=(('0','Base'),('1','Search Add View'),('2','Search View'),('3','View'))
    #customer_id = models.CharField(max_length=50,help_text='Customer ID')
    page = models.CharField(help_text='Page Name', max_length=100)
    url = models.CharField(help_text='Url', max_length=500,blank=True)
    page_description = models.TextField(blank=True,null=True,help_text='Description')
    short_description = models.CharField(max_length=30,blank=True,null=True,help_text='Short Description')
    page_category= models.CharField(choices=page_category_choices, max_length=20, default='1',help_text='Page Mode')
    audit_name = models.CharField(help_text='Audit Name',max_length=30,blank=True)
    audit_dttm=models.DateTimeField(blank=True, null=True,help_text='Audit DateTime')

    data = HStoreField(null = True)

    def __unicode__(self):
        return str(self.page)

    class Meta:
        db_table="sunrise_contrib_authentication_pagegroup"
        unique_together=('url','page')


class SunriseRole(models.Model):
    ROLE_STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    #customer_id = models.CharField(max_length=50,help_text='Customer ID')
    id = models.AutoField(primary_key=True,help_text='ID')
    role_nm= models.CharField(help_text='Role ID', max_length=50)
    description = models.TextField(help_text='Description',blank=True)
    status = models.CharField(help_text='Status', choices=ROLE_STATUS, max_length=10,default='Active')
    is_support_admin=models.BooleanField(default=False,help_text='Is Support Admin')
    pages=models.ManyToManyField(PageGroup, through='RolePageAccess',help_text='Page Group')
    audit_name = models.CharField(help_text='Audit Name',max_length=30,blank=True)
    audit_dttm=models.DateTimeField(blank=True, null=True,help_text='Audit DateTime')

    data = HStoreField(null = True)


    def __unicode__(self):
        return str(self.role_nm)

    class Meta:
        db_table="sunrise_contrib_authentication_sunriserole"
        #unique_together=('customer_id','role_nm')

class SunriseProfile(AbstractBaseUser):

    LOGIN_VIA = (
        ('Inbuilt', 'Hosted Website'),
        ('LDAP', 'LDAP'),
    )
    username = models.CharField(max_length = 30, unique = True)
    first_name = models.CharField(max_length = 30, blank = True)
    last_name = models.CharField(max_length = 30, blank = True)
    email = models.EmailField()
    is_active = models.BooleanField(default = True)
    control_access = models.BooleanField(default = False)
    change_password_after = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    #customer_id = models.ForeignKey(Customer,help_text='Customer ID_ID', null = True)
    description = models.CharField(help_text='Description', max_length=50,blank=True)
    login_via = models.CharField(help_text='Log-In via', choices=LOGIN_VIA, max_length=20,default='Inbuilt')
    lockout_account = models.BooleanField(default=False,help_text='Lock-Out Account')
    password_expired = models.BooleanField(default=False,help_text='Is Password Active?')
    rec_sys_not =  models.BooleanField(help_text='Receive System Notifications', default = False)
    title = models.CharField(max_length = 30, null = True, blank = True,help_text='Title')
    roles=models.ManyToManyField(SunriseRole, through='SunriseProfileRolesAssigned',help_text='Role')
    login_attempts = models.PositiveSmallIntegerField(default=0,help_text='')
    enable_trace_opt = models.BooleanField(help_text='Enable tracing options', default = False)
    pwd_expire_from = models.DateTimeField(blank=True,null=True,help_text='Password Valid From')
    pwd_expire_to = models.DateTimeField(blank=True,null=True,help_text='Password Valid To')
    pwd_hint = models.CharField(max_length=30,blank=True,null=True,help_text='Password Hint')
    otp_attempts = models.PositiveSmallIntegerField(default=0,help_text='')
    audit_name=models.CharField('Last Updated By:',max_length=30,blank=True,help_text='Audit Name')
    audit_dttm=models.DateTimeField(blank=True, null=True,help_text='Audit DateTime')

    data = HStoreField(null = True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __unicode__(self):
        return str(self.username)

    class Meta:
        db_table="sunrise_contrib_authentication_sunriseprofile"

class RolePageAccess(models.Model):
    ACCESS_TYPE = (
        ('R', 'View'),
        ('U', 'Add/Update'),
    )
    page = models.ForeignKey(PageGroup,help_text='Page_ID')
    role = models.ForeignKey(SunriseRole,related_name='access_of_pages',help_text='Role_ID')
    access_type = models.CharField(help_text='Access Type', choices=ACCESS_TYPE, max_length=12,default='R')
    is_active = models.BooleanField(default=True,help_text='Is Active')
    # functional_areas = models.ManyToManyField(FunctionalArea, through='RolePageFunctionalAreaAccess',help_text='Functional Areas' )
    data = HStoreField(null = True)

    class Meta:
        db_table="sunrise_contrib_authentication_rolepageaccess"


class SunriseProfileRolesAssigned(models.Model):
    profile=models.ForeignKey(SunriseProfile,related_name='assigned_roles',help_text='Profile_ID')
    role=models.ForeignKey(SunriseRole,help_text='Role_ID')
    data = HStoreField(null = True)

    def __unicode__(self):
        return str(self.id)
    class Meta:
        db_table="sunrise_contrib_authentication_sunriseprofilerolesassigned"

class SearchCriteria(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100, null = True, blank = True)
    type = models.CharField(max_length = 10, default = "Public", choices = (('Private', 'Private'), ('Public', 'Public')))
    created_by = models.CharField(max_length = 100, null = True, blank = True)
    url = models.CharField(max_length = 100)
    data = HStoreField(null = True)

    class Meta:
        db_table = "sunrise_contrib_search_criteria"  


class OldPasswords(models.Model):
    user = models.ForeignKey(SunriseProfile)
    pwds = models.CharField(max_length=200)   
    audit_dttm = models.DateTimeField(blank=True,null=True)
    audit_user = models.CharField(max_length=100,blank=True,null=True) 
    def checkLastFourPasswords(self, user, password,n):
        _passwords = OldPasswords.objects.filter(user = user).values("pwds").order_by("-pk")[:n]
        _found = False
        for pwd in _passwords:
            if check_password(password, pwd['pwds']):
                _found = True
                break

        return _found    
         
