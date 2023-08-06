""" This is the Custom Pagination """
# Author: partha

import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class PageNumberPaginationDataOnly(PageNumberPagination):
    """ Custom pagination """
    page_size_query_param = 'page_size'

    @property
    def page_size(self):
        """ return the page_size """
        return self.page_size

    @page_size.setter
    def page_size(self, value):
        self.page_size = value

    @property
    def low_bound(self):
        """ return the low_bound """
        return self.low_bound

    @low_bound.setter
    def low_bound(self, value):
        self.low_bound = value

    @property
    def total_bound(self):
        """ total items """
        return self.total_bound

    @total_bound.setter
    def total_bound(self, value):
        return self.total_bound

    @property
    def up_bound(self):
        """ upper bound """
        return self.up_bound

    @up_bound.setter
    def up_bound(self):
        return self.up_bound

    @property
    def low_bound_next(self):
        """ next upper bound """
        return self.low_bound_next

    @low_bound_next.setter
    def low_bound_next(self, value):
        self.low_bound_next = value

    @property
    def low_bound_prev(self):
        """ Previous lower bound """
        return self.low_bound_prev

    @low_bound_prev.setter
    def low_bound_prev(self, value):
        self.low_bound_prev = value

    @property
    def start_num(self):
        """ start bound """
        return self.start_num

    @start_num.setter
    def start_num(self, value):
        self.start_num = value

    @property
    def end_num(self):
        """ last bound """
        return self.end_num

    @end_num.setter
    def end_num(self, value):
        self.end_num = value

    @property
    def total_num(self):
        """ total bounds """
        return self.total_num

    @total_num.setter
    def total_num(self, value):
        self.total_num = value

    @property
    def request(self):
        """ total bounds """
        return request

    @request.setter
    def request(self, value):
        self.request = value

    @property
    def page(self):
        """ page """
        return self.page

    @page.setter
    def page(self, value):
        self.page = value

    @property
    def display_page_controls(self):
        """ Used for control the page controls """
        return self.display_page_controls

    @display_page_controls.setter
    def display_page_controls(self, value):
        self.display_page_controls = value

    def paginate_queryset(
            self,
            queryset,
            request,
            view=None,
            cache_manager=None
    ):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        self.page_size = page_size
        if not page_size:
            return None
        self.low_bound = request.query_params.get('low_bound', None)
        if self.low_bound is not None:
            self.low_bound = int(self.low_bound)
            self.total_bound = len(queryset)
            try:
                sliced_result = cache_manager.getPageData(
                    self.low_bound, page_size)
                if len(queryset) > int(self.low_bound + page_size):
                    self.up_bound = int(self.low_bound + page_size)
                    self.low_bound_next = self.up_bound
                else:
                    self.up_bound = len(queryset)
                    self.low_bound_next = None
                if self.low_bound > page_size:
                    self.low_bound_prev = abs(self.low_bound - page_size)
                else:
                    if self.low_bound == 0:
                        self.low_bound_prev = None
                    else:
                        self.low_bound_prev = -1
            except Exception, general_exception:
                self.up_bound = len(queryset)
            self.request = request
            self.low_bound_prev = sliced_result[1]
            self.low_bound_next = sliced_result[2]
            self.start_num = sliced_result[3] + 1
            self.end_num = sliced_result[4]
            self.total_num = sliced_result[5]
            return list(sliced_result[0])
        else:
            paginator = self.django_paginator_class(queryset, page_size)
            page_number = request.query_params.get(self.page_query_param, 1)
            if page_number in self.last_page_strings:
                page_number = paginator.num_pages
            try:
                self.page = paginator.page(page_number)
            except InvalidPage as exc:
                msg = self.invalid_page_message.format(
                    page_number=page_number, message=six.text_type(exc)
                )
                raise NotFound(msg)

            if paginator.num_pages > 1 and self.template is not None:
                # The browsable API should display pagination controls.
                self.display_page_controls = True

            self.request = request
            return list(self.page)

    def get_paginated_response(self, data):
        """ To paginate the reseponse content """
        if self.low_bound is not None:

            if self.low_bound_next is not None:
                _next = self.get_next_link()
            else:
                _next = None
            if self.low_bound_prev is not None:
                _prev = self.get_previous_link()
            else:
                _prev = None

            return Response({
                'links': {
                    'next': _next,
                    'previous': _prev
                },
                'pagination': {
                    'total_num': self.total_num,
                    'total_pages': int(math.ceil(float(float(self.total_bound) / self.page_size))),
                    'end_num': self.end_num,
                    'start_num': self.start_num,
                    'first': 1,
                    'last': int(math.ceil(float(float(self.total_bound) / self.page_size))),
                    'low_bound_prev': self.low_bound_prev,
                    'low_bound_next': self.low_bound_next,
                    'last_url': self.get_last_link()
                },
                'results': data
            })
        else:
            if self.page.number == 1:
                start_num = 1
            else:
                start_num = ((self.page.number - 1) *
                             self.page.paginator.per_page) + 1
            end_num = self.page.number * self.page.paginator.per_page

            if end_num > self.page.paginator.count:
                end_num = self.page.paginator.count
            if self.page.number == 2:
                prev_link = self.get_previous_link()
            else:
                prev_link = self.get_previous_link()
            return Response({
                'links': {
                    'next': self.get_next_link(),
                    'previous': prev_link,
                    'last_url': self.get_last_link()
                },
                'pagination': {
                    'total_num': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages,
                    'end_num': end_num,
                    'start_num': start_num,
                    'first': self.page.start_index(),
                    'last': self.page.paginator.count,
                },
                'results': data
            })

    def get_next_link(self):
        """ to get the next page link """
        url = self.request.build_absolute_uri()
        url = remove_query_param(url, 'page_size')
        url = remove_query_param(url, 'low_bound')
        url = remove_query_param(url, 'page')
        url = remove_query_param(url, 'sort')
        url = remove_query_param(url, 'refresh')

        if self.low_bound is not None:
            return url

        if not self.page.has_next():
            return None

        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        """ to get the previous page """
        url = self.request.build_absolute_uri()
        url = remove_query_param(url, 'page_size')
        url = remove_query_param(url, 'low_bound')
        url = remove_query_param(url, 'page')
        url = remove_query_param(url, 'sort')
        url = remove_query_param(url, 'refresh')

        if self.low_bound is not None:
            return url
        if not self.page.has_previous():
            return None

        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)

        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        """ To get the last page link """
        url = self.request.build_absolute_uri()
        url = remove_query_param(url, 'page_size')
        url = remove_query_param(url, 'low_bound')
        url = remove_query_param(url, 'page')
        url = remove_query_param(url, 'sort')
        url = remove_query_param(url, 'refresh')

        if self.low_bound is not None:
            return url
        return replace_query_param(url, self.page_query_param, 'last')


class CustomGridNavigation(PageNumberPagination):
    """ For a custom data pagination mechanism """

    page_size_query_param = 'page_size'
    @property
    def page_size(self):
        """ return the page_size """
        return self.page_size

    @page_size.setter
    def page_size(self, value):
        self.page_size = value

    @property
    def low_bound(self):
        """ return the low_bound """
        return self.low_bound

    @low_bound.setter
    def low_bound(self, value):
        self.low_bound = value

    @property
    def total_bound(self):
        """ total items """
        return self.total_bound

    @total_bound.setter
    def total_bound(self, value):
        return self.total_bound

    @property
    def up_bound(self):
        """ upper bound """
        return self.up_bound

    @up_bound.setter
    def up_bound(self):
        return self.up_bound

    @property
    def low_bound_next(self):
        """ next upper bound """
        return self.low_bound_next

    @low_bound_next.setter
    def low_bound_next(self, value):
        self.low_bound_next = value

    @property
    def low_bound_prev(self):
        """ Previous lower bound """
        return self.low_bound_prev

    @low_bound_prev.setter
    def low_bound_prev(self, value):
        self.low_bound_prev = value

    @property
    def start_num(self):
        """ start bound """
        return self.start_num

    @start_num.setter
    def start_num(self, value):
        self.start_num = value

    @property
    def end_num(self):
        """ last bound """
        return self.end_num

    @end_num.setter
    def end_num(self, value):
        self.end_num = value

    @property
    def total_num(self):
        """ total bounds """
        return self.total_num

    @total_num.setter
    def total_num(self, value):
        self.total_num = value

    @property
    def request(self):
        """ total bounds """
        return request

    @request.setter
    def request(self, value):
        self.request = value

    @property
    def page(self):
        """ page """
        return self.page

    @page.setter
    def page(self, value):
        self.page = value

    @property
    def display_page_controls(self):
        """ Used for control the page controls """
        return self.display_page_controls

    @display_page_controls.setter
    def display_page_controls(self, value):
        self.display_page_controls = value

    def paginate_queryset(self, queryset, request, view=None, cache_manager=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        self.page_size = page_size
        if not page_size:
            return None
        self.low_bound = request.query_params.get('low_bound', None)
        if self.low_bound is not None and self.low_bound != "NaN":
            self.low_bound = int(self.low_bound)
            self.total_bound = len(queryset)
            try:
                sliced_result = cache_manager.getPageData(
                    self.low_bound, page_size)
                if len(queryset) > int(self.low_bound + page_size):
                    self.up_bound = int(self.low_bound + page_size)
                    self.low_bound_next = self.up_bound
                else:
                    self.up_bound = len(queryset)
                    self.low_bound_next = None
                if self.low_bound > page_size:
                    self.low_bound_prev = abs(self.low_bound - page_size)
                else:
                    if self.low_bound == 0:
                        self.low_bound_prev = None
                    else:
                        self.low_bound_prev = -1
            except:
                self.up_bound = len(queryset)
            self.request = request
            self.low_bound_prev = sliced_result[1]
            self.low_bound_next = sliced_result[2]
            self.start_num = sliced_result[3] + 1
            self.end_num = sliced_result[4]
            self.total_num = sliced_result[5]
            return list(sliced_result[0])
        else:
            paginator = self.django_paginator_class(queryset, page_size)
            page_number = request.query_params.get(self.page_query_param, 1)
            if page_number in self.last_page_strings:
                page_number = paginator.num_pages
            try:
                self.page = paginator.page(page_number)
            except InvalidPage as exc:
                msg = self.invalid_page_message.format(
                    page_number=page_number, message=six.text_type(exc)
                )
                raise NotFound(msg)

            if paginator.num_pages > 1 and self.template is not None:
                # The browsable API should display pagination controls.
                self.display_page_controls = True

            self.request = request
            return list(self.page)

    def get_paginated_response(self, data):
        """ to paginate the response """
        if self.page.number == 1:
            start_num = 1
        else:
            start_num = ((self.page.number - 1) *
                         self.page.paginator.per_page) + 1
        end_num = self.page.number * self.page.paginator.per_page

        if end_num > self.page.paginator.count:
            end_num = self.page.paginator.count
        if self.page.number == 2:
            prev_link = self.get_previous_link()
        else:
            prev_link = self.get_previous_link()
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': prev_link,
                'last_url': self.get_last_link()
            },
            'pagination': {
                'total_num': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'end_num': end_num,
                'start_num': start_num,
                'first': self.page.start_index(),
                'last': self.page.paginator.count,
            },
            'results': data
        })

    def get_next_link(self):
        """ To get the next page link """
        url = self.request.build_absolute_uri()
        url = replace_query_param(
            url, 'page_size', self.request.GET.get('page_size', 5))
        url = remove_query_param(url, 'low_bound')
        url = replace_query_param(
            url, 'sort', self.request.GET.get('sort', ''))
        url = replace_query_param(
            url, 'query', self.request.GET.get('query', ''))

        # if self.low_bound is not None and self.low_bound != "Nan":
        #     return url

        if not self.page.has_next():
            return None

        page_number = self.page.next_page_number()
        print self.page_query_param
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        """ To get the previous page link """
        url = self.request.build_absolute_uri()
        url = replace_query_param(
            url, 'page_size', self.request.GET.get('page_size', 5))
        url = remove_query_param(url, 'low_bound')
        url = replace_query_param(
            url, 'sort', self.request.GET.get('sort', ''))
        url = replace_query_param(
            url, 'query', self.request.GET.get('query', ''))

        if self.low_bound is not None and self.low_bound != "Nan":
            return url
        if not self.page.has_previous():
            return None

        page_number = self.page.previous_page_number()
        if page_number == 1:
            return replace_query_param(url, self.page_query_param, page_number)

        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        """ To get the last page link """
        url = self.request.build_absolute_uri()
        url = replace_query_param(
            url, 'page_size', self.request.GET.get('page_size', 5))
        url = remove_query_param(url, 'low_bound')
        url = replace_query_param(
            url, 'sort', self.request.GET.get('sort', ''))
        url = replace_query_param(
            url, 'query', self.request.GET.get('query', ''))

        if self.low_bound is not None and self.low_bound != "Nan":
            return url
        return replace_query_param(url, self.page_query_param, 'last')
