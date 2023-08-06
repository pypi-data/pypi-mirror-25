# Author: Integra
# Dev: Partha

import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from rest_framework import viewsets,status
from rest_framework import pagination

from sunrise.pages.search_add_view import SearchAddView
from sunrise.pages.category import Category1

from .models import Addon, AddonHistory

class AddonPage(SearchAddView):
    pass

class MenuBuilder(SearchAddView):
    pass
    

