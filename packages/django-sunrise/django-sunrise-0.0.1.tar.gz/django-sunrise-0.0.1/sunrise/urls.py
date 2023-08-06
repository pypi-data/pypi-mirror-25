from django.conf.urls import include, url
from django_mfa.views import configure_mfa_email, enable_mfa_initial
from sunrise.contrib.addons import urls as addon_urls
from sunrise.contrib.oauth import urls as oauth_urls
from sunrise.contrib.authentication.views import PasswordResetConfirm,ForgotPassword,PasswordPreferences,changePassword,SendEmail
#Routes
from sunrise.contrib.authentication import urls as authentication_urls
from sunrise.contrib.jobs import urls as jobs_urls
from sunrise.contrib.authentication import routes as authentication_routes
from sunrise.contrib.addons import routes as menu_routes
from sunrise.contrib.oauth import routes as oauth_routes
from sunrise.contrib.jobs import routes as jobs_routes

#Including Login Urls
from sunrise.contrib.authentication import login_urls

#Themes
from sunrise.contrib.notifications.views import get_themes, updateThemePreferences, get_user_preferences
from sunrise.contrib.jobs.views import RequestHeader
from .views import base_view, PageCacheView

urlpatterns = [    
    #Themes
    url(r'^api/get_themes/$', get_themes),
    url(r'^api/update_preferences/$', updateThemePreferences),
    url(r'^api/get_preferences/$', get_user_preferences),
    # Account & Security
    url(r'^accounts/', include(login_urls)),
    url(r'^password_preferences/', PasswordPreferences.as_view()),
    url(r'^forgot_password/', ForgotPassword.as_view()), 
    url(r'^send_email/', SendEmail),
    url(r'^change_password/',changePassword),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_confirm',PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    #mfa setup url
    url(r'^mfa_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',configure_mfa_email, name='mfa_confirm_email'),
    url(r'^enable_mfa_initial/', enable_mfa_initial, name='enable_mfa_initial'),
    #SetupUrls
    url(r'^setup/', include(authentication_urls)),
    url(r'^setup/', include(jobs_urls)),
    url(r'^setup/', include(oauth_urls)), 
    #SetupRoutes
    url(r'^api/setup/', include(menu_routes)),
    url(r'^api/setup/', include(authentication_routes)),
    url(r'^api/setup/', include(jobs_routes)), 
    #MFA Rules
    url(r'^settings/', include('django_mfa.urls', namespace="mfa")),
    #Docs
    url(r'^docs/', include('django_mkdocs.urls', namespace='documentation')),
    #Other
    url(r'^', include(addon_urls)),
    url(r'^_cache/set/(?P<dispatch>[\w-]+)/$', PageCacheView.as_view()),
    url(r'^_cache/get/(?P<dispatch>[\w-]+)/$', PageCacheView.as_view()), 
    #Oauth
    url(r'^api/oauth/', include(oauth_routes)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #Cloud
    url(r'^storage/', include('sunrise.contrib.cloud.urls', namespace='storage')),       
]
