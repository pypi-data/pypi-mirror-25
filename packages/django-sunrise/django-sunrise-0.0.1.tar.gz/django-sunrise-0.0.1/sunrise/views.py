""" cache views """
# Author: partha

import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.generic import View
from sunrise.cache import PageCache, ResourceCache


def base_view(request):
    """ default Home Page """
    return render(request, "base.html", {})


class PageCacheBaseView(View):
    """ Cache set/get handlers """
    _GET_ACCEPTED = [
        'parent_pk',
        'initial_data',
        'next_search_key',
        'previous_search_key',
        'return_criteria'
    ]
    _POST_ACCEPTED = [
        'parent_pk',
        'initial_data'
    ]

    def get(
            self,
            request,
            dispatch=None
    ):
        """ For getting state """
        if dispatch not in self._GET_ACCEPTED:
            return HttpResponse(
                "Invalid Request",
                status=500
            )
        if dispatch == "parent_pk":
            return self.getParentPk(request)
        if dispatch == "initial_data":
            return self.getInitialData(request)
        if dispatch == "next_search_key":
            return self.getNextSearchKey(request)
        if dispatch == "previous_search_key":
            return self.getPreviousSearchKey(request)
        if dispatch == "return_criteria":
            return self.getReturnCriteria(request)

    def post(
            self,
            request,
            dispatch=None
    ):
        """ cache setters """
        if dispatch not in self._POST_ACCEPTED:
            return HttpResponse(
                "Invalid Request",
                status=500
            )

        if dispatch == "parent_pk":
            return self.set_parent_pk(request)
        if dispatch == "initial_data":
            return self.setInitialData(request)


class PageCacheView(PageCacheBaseView):
    """ Request Wrapper """

    def set_initial_data(
            self,
            request
    ):
        """ Used to set the initial data
            @params: data  """
        data = json.loads(request.body)['search']
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH']
        )
        cache_manager.set_initial_data(data)
        cache_manager.set(cache_manager.cache_key_parent_pk, None)
        cache_manager.set(cache_manager.cache_key_search_key, None)
        cache_manager.set(cache_manager.cache_key_search_list, None)
        return HttpResponse(True)

    def get_initial_data(
            self,
            request
    ):
        """ Used to return the initial data in add page """
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        data = cache_manager.get_initial_data()
        return HttpResponse(json.dumps(data))

    def set_parent_pk(
            self,
            request
    ):
        """ Used to set the parent pk in search list page @params': pk"""
        payload = json.loads(request.body)
        parent_pk = payload['pk']
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        try:
            cache_manager.set_search_key(parent_pk)
        except Exception, general_exception:
            pass
        cache_manager.set_parent_pk(parent_pk)
        _type = payload.get('type', 'basic')
        try:
            cache_manager.set_return_criteria(json.dumps(
                {'type': _type, 'criteria': payload['criteria']}))
        except Exception, general_exception:
            cache_manager.set_return_criteria(
                json.dumps({'type': _type, 'criteria': []}))
        return HttpResponse(True)

    def get_parent_pk(
            self,
            request
    ):
        """ Used to return the parent pkey in view page """
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        try:
            data = cache_manager.get_search_key()
        except Exception, general_exception:
            parent_pk = cache_manager.get(cache_manager.cache_key_parent_pk)
            data = (parent_pk, False, False)
        if data[0] is None:
            return HttpResponse("Page Not Found", status=404)
        return HttpResponse(json.dumps({'current': data[0], 'prev': data[1], 'next': data[2]}))

    def get_next_search_key(
            self,
            request
    ):
        """ Used to return next search key when you click on next """
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        data = cache_manager.get_next_key()
        return HttpResponse(
            json.dumps({
                'current': data[0],
                'prev': data[1],
                'next': data[2]
            })
        )

    def get_previous_search_key(
            self,
            request
    ):
        """ Used to return previous search when you click on previous """
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        data = cache_manager.get_prev_key()
        return HttpResponse(
            json.dumps({
                'current': data[0],
                'prev': data[1],
                'next': data[2]
            })
        )

    def get_return_criteria(
            self,
            request
    ):
        """ Used to get the return criteria """
        cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        data = cache_manager.get_return_criteria()
        return HttpResponse(data)


def handler404(request):
    """ 404 handler """
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    """ 500 handler """
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
