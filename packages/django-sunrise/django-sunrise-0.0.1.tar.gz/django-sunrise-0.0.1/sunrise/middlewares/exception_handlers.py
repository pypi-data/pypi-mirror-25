# Author: Integra
# Dev: Partha(Ref)

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, RequestContext, loader


def bad_request_handler(
        request,
        template_name='page_not_found.html'
):
    """ Bad Request (400) """
    return render(request, 'page_not_found.html', {})
 
def permission_denied_handler(
        request,
        template_name='403.html'
):
    """ Permission Denied (403) """
    return render(request, 'internal_server_error.html', {})

def page_not_found_handler(
        request,
        template_name='page_not_found.html'
):
    """ Page Not Found (404) """
    return render(request, 'page_not_found.html', {})

def server_error_handler(
        request,
        template_name='500.html'
):
    """ Internal Server Error (500) """
    return render(request, 'internal_server_error.html', {})
