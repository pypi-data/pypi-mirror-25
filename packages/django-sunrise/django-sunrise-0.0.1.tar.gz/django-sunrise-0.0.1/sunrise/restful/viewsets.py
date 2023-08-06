""" Custom viewset managers """
import datetime
import json
import StringIO
from itertools import chain
from operator import itemgetter

import xlsxwriter

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from sunrise.cache import MultiResourceCache, PageCache, ResourceCache
from sunrise.contrib.oauth.oauth_api import SunriseBillingAPI

from .pagination import CustomGridNavigation, PageNumberPaginationDataOnly


def get_all_subclasses(klass):
    """ return all subclasses of a class """
    all_subclasses = []
    for subclass in klass.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses


class ViewSetManager(viewsets.ModelViewSet):
    """ Custom viewset """
    ordering_fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Injecting plugins here
        plugins = get_all_subclasses(self.__class__)
        if len(plugins) > 0:
            self.__class__ = plugins[-1]
        super(ViewSetManager, self).__init__(*args, **kwargs)

    def _build_queryset(self, *args, **kwargs):
        return self.model.objects.all()

    def _initiate_cache_manager(self, grid_key=None):
        self.cache_manager = ResourceCache(
            UUID_HASH=self.request.session['UUID_HASH'],
            GRID_KEY=grid_key
        )

    def get_related_fkey(self, parent, child):
        """ will return the fkey between 2 models """
        fkey = None
        for field in child._meta.fields:
            if field.get_internal_type() == "ForeignKey" or field.get_internal_type() == "OneToOneField":
                if field.rel.to.__name__ == parent._meta.object_name:
                    fkey = field.name
                    break
        return fkey

    def get_serializer_class(self):
        serializer_class = self.parser['default']
        if getattr(self, 'action') in self.parser:
            serializer_class = self.parser[getattr(self, 'action')]

        if self.request.user is not None and self.request.user.is_superuser:
            if 'admin_' + getattr(self, 'action') in self.parser:
                serializer_class = self.parser['admin_' +
                                               getattr(self, 'action')]
        if self.action == 'download':
            if 'list' in self.parser.keys():
                serializer_class = self.parser['list']
            else:
                serializer_class = self.parser['default']
        # Check for the plugin extension
        plugins = get_all_subclasses(serializer_class)
        if len(plugins) > 0:
            return plugins[-1]
        return serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def SSLparse(self, ssl_string):
        """ ssl parser """
        ssl_string = ssl_string.replace("(", "Q(")
        ssl_string = ssl_string.replace(" AND ", ") & Q(")
        ssl_string = ssl_string.replace(" OR ", ") | Q(")
        ssl_string = ssl_string.replace(" and ", ") & Q(")
        ssl_string = ssl_string.replace(" or ", ") | Q(")
        return eval(ssl_string)

    def filtering(self, criteria, qset, search_type='basic', match_exact=False):
        """ basic filtering """
        _original_qset = qset
        if 'parent_pk' in self.request.GET.keys():
            if hasattr(self, 'parent'):
                fkey = self.get_related_fkey(self.parent, self.model)
                parent_pk = int(self.request.GET['parent_pk'])
                if parent_pk is not None:
                    _fkey_filter = {fkey: int(parent_pk)}
                    _original_qset = _original_qset.filter(**_fkey_filter)
        if hasattr(self, 'parent') and self.request.META.get('HTTP_X_GRIDKEY', None) != "lookup" and self.request.META.get('HTTP_X_GRIDKEY', None) != None or ((self.request.user is None or self.request.user.is_authenticated() == False) and self.request.auth is not None):
            fkey = self.get_related_fkey(self.parent, self.model)
            uuid_hash = self.request.session['UUID_HASH']
            page_cache_manager = PageCache().initiate(uuid_hash=uuid_hash)
            try:
                data = page_cache_manager.get_search_key()
                parent_pk = data[0]
            except Exception, general_exception:
                parent_pk = page_cache_manager.get(
                    page_cache_manager.cache_key_parent_pk)
            if 'parent_pk' in self.request.GET.keys():
                parent_pk = int(self.request.GET['parent_pk'])
            if parent_pk is not None:
                _fkey_filter = {fkey: int(parent_pk)}
                _original_qset = _original_qset.filter(**_fkey_filter)
            else:
                # Check for Oauth
                if (self.request.user is None or self.request.user.is_authenticated() == False) and self.request.auth is not None:
                    if 'parent_pk' in self.request.GET.keys():
                        _fkey_filter = {
                            fkey: int(self.request.GET['parent_pk'])}
                        return _original_qset.filter(**_fkey_filter)
                    else:
                        return _original_qset
                return _original_qset.filter(pk=-1)
        if criteria is not None:
            if search_type == 'basic':
                master_q = None
                for key, val in criteria.items():
                    slave_q = None
                    for item in val:
                        if match_exact:
                            try:
                                item = datetime.datetime.strptime(
                                    item, '%m/%d/%Y').date()
                            except:
                                pass
                            slave_q = Q(
                                **{key: item}) if slave_q is None else slave_q | Q(**{key: item})
                        else:
                            slave_q = Q(**{key + '__istartswith': item}) if slave_q is None else slave_q | Q(
                                **{key + '__istartswith': item})
                    if slave_q is not None:
                        master_q = slave_q if master_q is None else master_q & slave_q
                if master_q is not None:
                    if len(master_q) > 0:
                        return _original_qset.filter(master_q)
            if search_type == 'advanced':
                pass
            if search_type == 'ssl':
                return _original_qset.filter(self.SSLparse(criteria['criteria'].lstrip().rstrip()))
        return _original_qset

    def get_queryset(self, *args, **kwargs):
        """ Used to return the queryset """
        return []

    def _compare_dict(self, dict1, dict2):
        dict1_ = dict1.copy()
        dict2_ = dict2.copy()
        is_same = True
        for key in dict1_:
            if key in dict2_:
                # checking matching of each list of object
                if len(set(dict1_[key]) ^ set(dict2_[key])) > 0:
                    is_same = False
                    break
            else:
                is_same = False
                break
        return is_same

    def list(self, request, *args, **kwargs):
        """ Invoked for list of details """
        from_cached = False
        _criteria = None
        navigation_flag = False
        # grid prefix

        _grid_key = self.request.META.get('HTTP_X_GRIDKEY', None)
        # 1. Check whether calling for the first time
        self._initiate_cache_manager(grid_key=_grid_key)
        page_cache_manager = PageCache().initiate(
            uuid_hash=request.session['UUID_HASH'])
        if request.method == "GET":
            payload = request.GET
        else:
            payload = request.POST

        if 'refresh' in payload and payload['refresh'] != "":
            self.cache_manager.refresh_cache()
            data = self.cache_manager.get_data()
        if 'page' in payload and payload['page'] != "":
            data = self.cache_manager.get_data()
            from_cached = True
        if 'low_bound' in payload and payload['low_bound'] != "":
            data = self.cache_manager.get_data()
            from_cached = True
        if 'match_exact' in payload and payload['match_exact'] != "":
            from_cached = False
            navigation_flag = True
            _criteria = json.loads(payload['search'])

        if 'search' in payload and payload['search'] != "" and navigation_flag is False:
            # 1. Get existing criteria
            existing_criteria = self.cache_manager.get_search_params()
            new_criteria = json.loads(payload['search'])
            # 2. If no criterial previously then build the queryset
            if existing_criteria is None:
                _criteria = new_criteria
                self.cache_manager.set_search_params(_criteria)
                from_cached = False
            else:
                # 3. Compare with the new
                matched_items = self._compare_dict(existing_criteria, new_criteria)
                if matched_items is True:
                    from_cached = True
                else:
                    # 5. If both are not same then build the queryset and update the cache_key_criteria
                    _criteria = new_criteria
                    self.cache_manager.set_search_params(_criteria)
                    from_cached = False
            if from_cached is True:
                data = self.cache_manager.get_data()
        if 'return' in payload and payload['return'] == "true":
            _criteria = self.cache_manager.get_search_params()
            from_cached = False

        if 'sort' in payload and payload['sort'] != "":
            sortval = payload['sort']
            if sortval[0] == '-':
                sortname = sortval[1:]
                sortorder = False
            else:
                sortname = sortval
                sortorder = True
            data = self.cache_manager.sort_cache(sortname, sortorder)
            data = self.cache_manager.get_data()
            from_cached = True
            # 1.check active catch if it is filter make sort as active cache .
            # 2.if active catch is sort then just sort the data.
        if not from_cached:
            # 2. Initiate ResourceCache using cache_key
            self.cache_manager.register_cache_state_keys()
            # 3. set cache data for the grid
            qset = self.model.objects.all()
            if hasattr(self, 'filtering'):
                search_type = 'basic'
                if 'search_type' in payload and payload['search_type'] != "":
                    search_type = payload['search_type']
                try:
                    qset = self.filtering(
                        _criteria, qset, search_type, navigation_flag)
                except Exception, e:
                    print str(e)
                    pass
            self.cache_manager.set_grid_cache_data(qset=qset)
            # Set the autofill data
            if 'autofill' in payload.keys() and payload['autofill'] == "true":
                self._auto_fill(
                    self.cache_manager, initial_data=page_cache_manager.get_initial_data())
            # 4. Get the data from the cache manager
            data = self.cache_manager.get_data()
            # 5. Set search list
        if _grid_key is None:
            # This will be set for search page grids only
            page_cache_manager.set_search_list(
                self.model._meta.pk.name, self.cache_manager.cache_key_active)
        # 5. Paginate the data
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self, cache_manager=self.cache_manager)

    def get_object(self, pk=None):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if pk is None:
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        else:
            filter_kwargs = {self.lookup_field: pk}
        try:
            obj = self.model.objects.filter(**filter_kwargs)[0]
        except (TypeError, ValueError, IndexError):
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """ Invoked on Create """
        if 'data' in kwargs and kwargs['data'] is not None:
            data = kwargs['data']
        else:
            data = request.data
        if hasattr(self, 'populate'):
            data = self.populate(request, request.data, 'create')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.object = serializer.save()
            if hasattr(self, 'post_save'):
                self.post_save(request, self.object, created=True, data=data)
            headers = self.get_success_headers(serializer.data)
            if request.accepted_renderer.format == 'json':
                return Response({'result': serializer.data, 'lookup_field': self.lookup_field, 'resource_uri': request.path + str(getattr(self.object, self.lookup_field)) + '/', 'pk': str(getattr(self.object, self.lookup_field))}, status=status.HTTP_201_CREATED, headers=headers)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ Invoked on the update of the records """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        previous_data = instance.__dict__

        if 'data' in kwargs and kwargs['data'] is not None:
            data = kwargs['data']
        else:
            data = request.data
        for key, val in previous_data.items():
            if key in data.keys():
                if previous_data[key] == data[key]:
                    data.pop(key, None)
        if hasattr(self, 'populate'):
            data = self.populate(request, request.data, 'update')
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if hasattr(self, 'post_save'):
            self.post_save(request, instance, created=False, data=data)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ Invoked for the detail record """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """ Invoked for the delete of the resource """
        instance = self.get_object()
        self.perform_destroy(instance)

    def _auto_fill(self, cache_manager, initial_data=None):
        """ Used to fill the cache with the prepopulated data """
        if hasattr(self, 'auto_fill'):
            auto_fill_data = self.auto_fill(initial_data=initial_data)
            if isinstance(auto_fill_data, QuerySet) is True:
                auto_fill_data = list(auto_fill_data.values())
            _populated_data = []
            for _idx, every_row in enumerate(auto_fill_data):
                # Add entry in Cache
                at_grid_index = _idx - 1
                fields = self.get_serializer_class()().fields.keys()
                grid_index = cache_manager.addItem(at_grid_index, fields)
                # Update data
                every_row.update({'grid_index': grid_index})
                _populated_data.append(every_row)
            _updated = cache_manager.updateItem(_populated_data)
        return Response({"status": True})

    @detail_route()
    def retrieve_from_parent(self, request, pk=None):
        """ This is used to return the child detail using parent pk """
        if hasattr(self, 'parent'):
            fkey = self.get_related_fkey(self.parent, self.model)
            _criteria = {fkey: int(pk)}
            qset = self.model.objects.filter(**_criteria)
            if len(qset) > 0:
                serializer = self.get_serializer(qset[0])
                return Response(serializer.data)
            else:
                return Response({})
        else:
            return Response({})

    @detail_route()
    def retrieve_childs(self, request, pk=None):
        """ This is used to return the child detail using parent pk """
        if hasattr(self, 'parent'):
            fkey = self.get_related_fkey(self.parent, self.model)
            _criteria = {fkey: int(pk)}
            qset = self.model.objects.filter(**_criteria).order_by("-pk")
            if len(qset) > 0:
                serializer = self.get_serializer(qset, many=True)
                return Response(serializer.data)
            else:
                return Response({})
        else:
            return Response({})

    @list_route()
    def add_item(self, *args, **kwargs):
        """ List route for add item """
        at_grid_index = self.request.GET.get('at_grid_index', None)
        _grid_key = self.request.META['HTTP_X_GRIDKEY']
        self._initiate_cache_manager(grid_key=_grid_key)
        fields = self.get_serializer_class()().fields.keys()
        grid_index = self.cache_manager.addItem(at_grid_index, fields)
        return Response({"grid_index": grid_index})

    @list_route()
    def delete_item(self, *args, **kwargs):
        """ List route for delete item """
        _grid_key = self.request.META['HTTP_X_GRIDKEY']
        self._initiate_cache_manager(grid_key=_grid_key)
        grid_index = self.request.GET['grid_index']
        if 'low_bound' in self.request.GET and self.request.GET['low_bound'] != "":
            low_bound = self.request.GET['low_bound']
        else:
            low_bound = None
        # Hardcoding for testing purpose : Get it from request
        nextRow = self.cache_manager.deleteItem(int(grid_index), low_bound)
        if nextRow[0] is not None:
            try:
                self.action = 'list'
                data = self.get_serializer(nextRow[0]).data
            except:
                data = None
        else:
            data = None
        return Response({"status": data, 'low_bound_next': nextRow[1]})

    @list_route(methods=['post'])
    def update_items(self, *args, **kwargs):
        """ List route for update item """
        _grid_key = self.request.META['HTTP_X_GRIDKEY']
        self._initiate_cache_manager(grid_key=_grid_key)
        _populated_data = []
        if hasattr(self, 'populate'):
            _populated_data = []
            for _data in self.request.data['data']:
                _populated_data.append(
                    self.populate(self.request, _data, True))
        else:
            _populated_data = self.request.data['data']
        return Response({'status': self.cache_manager.updateItem(_populated_data)})

    @list_route()
    def refresh_items(self, *args, **kwargs):
        """ Invoked when refresh triggered """
        return Response({"status": "ok"})

    @list_route()
    def download(self, *args, **kwargs):
        """ Invoked when download triggered """
        _grid_key = self.request.GET.get('GridKey', None)
        self._initiate_cache_manager(grid_key=_grid_key)
        data = self.cache_manager.get_data()
        serializer = self.get_serializer(data, many=True)
        outputdata = serializer.data
        fields = json.loads(self.request.GET['fields'])
        headings = json.loads(self.request.GET['header'])
        file_name = self.request.GET['file_name']
        response = HttpResponse(
            content_type="application/openxmlformats-officedocument.spreadsheetml.sheet")
        file_name = file_name + '_' + datetime.datetime.now().strftime('%m_%d_%y %I:%M %p')
        response['Content-Disposition'] = 'attachment; filename="' + \
            file_name + '.xlsx"'
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'default_date_format': 'dd/mm/yy'})
        sheet = workbook.add_worksheet('worksheet')
        header_format = workbook.add_format(
            {'bold': True, 'font_name': 'Times New Roman'})
        date_format = workbook.add_format(
            {'bold': False, 'num_format': 'mm/dd/yy', 'font_name': 'Times New Roman'})
        datetime_format = workbook.add_format(
            {'bold': False, 'num_format': 'mm/dd/yy hh:mm AM/PM', 'font_name': 'Times New Roman'})
        row_format = workbook.add_format(
            {'bold': False, 'font_name': 'Times New Roman'})
        row = 0
        # Write Headings
        for column, heading in enumerate(headings):
            heading = heading[1:len(heading)] if heading.startswith(
                '*', 0) else heading
            sheet.write(row, column, heading, header_format)
        # Write Data
        for record in outputdata:
            row = row + 1
            for idx, field in enumerate(fields):
                if field in record.keys():
                    sheet.write(row, idx, record[field], row_format)
        workbook.close()
        response.write(output.getvalue())
        return response

    @list_route()
    def save(self, *args, **kwargs):
        # 1. Get cache Manager
        env_keys = {
            'session_key': kwargs.get('session_key', None),
            'tab_key': kwargs.get('tab_key', None),
            'grid_key': kwargs.get('grid_key', None),
        }
        self._initiate_cache_manager(**env_keys)
        # 2. Get items to delete
        items_to_delete = self.cache_manager.items_to_delete
        # 3. Get items to update
        items_to_update = self.cache_manager.items_to_update
        # 4. Get items to add
        items_to_add = self.cache_manager.items_to_add

        # 5. deleting all items_to_delete
        for item in items_to_delete:
            # need to get pk field dynamically
            if "id" in item and item['id'] != "":
                toDelObj = self.model.objects.get(
                    pk=item['id'])  # need to improve no of hits
                toDelObj.delete()
        # 6. Update all items in items_to_update
        for item in items_to_update:
            if "id" in item:
                # Remove the material keys
                material_keys = ["row_bound_status",
                                 "row_added_status", "grid_index"]
                temp = [item.pop(key, None) for key in material_keys]
                #Validating and updating
                partial = kwargs.pop('partial', False)
                instance = self.model.objects.get(pk=item['id'][0])
                data = {}
                for key, val in item.items():
                    if val[1] == 'unbound':
                        data.update({key: val[0]})
                if hasattr(self, 'populate'):
                    data = self.populate(self.request, data, 'update')
                serializer = self.get_serializer(
                    instance, data=data, partial=partial)
                serializer.is_valid(raise_exception=True)
                instance = self.perform_update(serializer)
                if hasattr(self, 'post_save'):
                    self.post_save(self.request, instance,
                                   created=False, data=data)
        # 7. Add all items in items_to_add
        for item in items_to_add:
            material_keys = ["row_bound_status",
                             "row_added_status", "grid_index"]
            temp = [item.pop(key, None) for key in material_keys]
            data = {}
            for key, val in item.items():
                if val is not None and type(val) == tuple:
                    data.update({key: val[0]})
            if hasattr(self, 'populate'):
                data = self.populate(self.request, data, 'create')
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.object = serializer.save()
                if hasattr(self, 'post_save'):
                    self.post_save(self.request, self.object,
                                   created=True, data=data)
        # 8. Removing cache contents of modified, deleted
        self.cache_manager.ceil_cache()
        return Response({'status': 'records saved successfully'})

    @list_route()
    def debug(self, *args, **kwargs):
        _grid_key = self.request.META['HTTP_X_GRIDKEY']
        self._initiate_cache_manager(grid_key=_grid_key)
        data = self.cache_manager.debug
        return Response(data)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        ###
        # added in compatibility with lookup field
        if 'pk' in kwargs:
            try:
                kwargs['pk'] = int(kwargs['pk'])
            except:
                pass

        ###
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)
        return self.response


class MultiResourceAPIView(APIView):
    """ For handling custom data """
    paginator = PageNumberPaginationDataOnly()

    def get_data(self, request, *args, **kwargs):
        """ Need to be overriden by the dev """
        raise NotImplementedError

    def _initiate_cache_manager(self, grid_key=None):
        if 'UUID_HASH' not in self.request.session.keys():
            self.request.session['UUID_HASH'] = self.request.session.session_key + "_dashboard"
        self.cache_manager = MultiResourceCache(
            uuid_hash=self.request.session['UUID_HASH'], GRID_KEY=grid_key)

    def paginate_queryset(self, data):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(data, self.request, view=self, cache_manager=self.cache_manager)

    def download(self, request):
        _grid_key = self.request.GET.get('GridKey', None)
        self._initiate_cache_manager(grid_key=_grid_key)
        data = self.cache_manager.get_data()
        # serializer = self.get_serializer(data, many=True)
        outputdata = data
        fields = json.loads(self.request.GET['fields'])
        headings = json.loads(self.request.GET['header'])
        file_name = self.request.GET['file_name']
        response = HttpResponse(
            content_type="application/openxmlformats-officedocument.spreadsheetml.sheet")
        file_name = file_name + '_' + datetime.datetime.now().strftime('%m_%d_%y %I:%M %p')
        response['Content-Disposition'] = 'attachment; filename="' + \
            file_name + '.xlsx"'
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'default_date_format': 'dd/mm/yy'})
        sheet = workbook.add_worksheet('worksheet')
        header_format = workbook.add_format(
            {'bold': True, 'font_name': 'Times New Roman'})
        date_format = workbook.add_format(
            {'bold': False, 'num_format': 'mm/dd/yy', 'font_name': 'Times New Roman'})
        datetime_format = workbook.add_format(
            {'bold': False, 'num_format': 'mm/dd/yy hh:mm AM/PM', 'font_name': 'Times New Roman'})
        row_format = workbook.add_format(
            {'bold': False, 'font_name': 'Times New Roman'})
        row = 0
        # Write Headings
        for column, heading in enumerate(headings):
            heading = heading[1:len(heading)] if heading.startswith(
                '*', 0) else heading
            sheet.write(row, column, heading, header_format)
        # Write Data

        for record in outputdata:
            row = row + 1
            for idx, field in enumerate(fields):
                if field in record.keys():
                    try:
                        sheet.write(row, idx, record[field], row_format)
                    except:
                        sheet.write(
                            row, idx, record[field].__str__(), row_format)
        workbook.close()
        response.write(output.getvalue())
        return response

    def get(self, request, *args, **kwargs):
        if request.path.endswith("/download/"):
            return self.download(request)
        output = []
        page = 1
        from_cached = False
        _grid_key = self.request.META.get('HTTP_X_GRIDKEY', None)
        self._initiate_cache_manager(grid_key=_grid_key)
        payload = request.GET

        # Check for page
        if 'page' in payload.keys() and payload['page'] != "":
            page = payload['page']
            data = self.cache_manager.get_data()
            from_cached = True

        # Check for sort
        if 'sort' in payload.keys() and payload['sort'] != "":
            sortval = payload['sort']
            if sortval[0] == '-':
                sortname = sortval[1:]
                sortorder = False
            else:
                sortname = sortval
                sortorder = True
            data = self.cache_manager.sort_cache(sortname, sortorder)
            data = self.cache_manager.get_data()
            from_cached = True

        # Check for page_size
        if 'page_size' in payload and payload['page_size'] != "":
            page_size = payload['page_size']

        if 'search' in payload and payload['search'] != "" and navigation_flag is False:
            # 1. Get existing criteria
            existing_criteria = self.cache_manager.get_search_params()
            new_criteria = json.loads(payload['search'])
            # 2. If no criterial previously then build the queryset
            if existing_criteria is None:
                _criteria = new_criteria
                self.cache_manager.set_search_params(_criteria)
                from_cached = False
            else:
                # 3. Compare with the new
                matched_items = self._compare_dict(existing_criteria, new_criteria)
                if matched_items is True:
                    from_cached = True
                else:
                    # 5. If both are not same then build the queryset and update the cache_key_criteria
                    _criteria = new_criteria
                    self.cache_manager.set_search_params(_criteria)
                    from_cached = False
            if from_cached is True:
                data = self.cache_manager.get_data()

        if not from_cached:
            self.cache_manager.register_cache_state_keys()
            # 3. set cache data for the grid
            data = self.get_data(request, *args, **kwargs)
            data = data['data']
            fields = data['fields']
            self.cache_manager.set_grid_cache_data(data=data, fields=fields)
            # 4. Get the data from the cache manager
            data = self.cache_manager.get_data()
            self.request.GET._mutable = True
            self.request.GET.pop('low_bound', None)
        page = self.paginate_queryset(data)
        return self.paginator.get_paginated_response(page)

    def post(self, request, *args, **kwargs):
        output = []
        page = 1
        from_cached = False
        _grid_key = self.request.META.get('HTTP_X_GRIDKEY', None)
        self._initiate_cache_manager(grid_key=_grid_key)
        payload = request.POST

        # Check for page
        if 'page' in payload.keys() and payload['page'] != "":
            page = payload['page']

        # Check for sort
        if 'sort' in payload.keys() and payload['sort'] != "":
            sort = payload['sort']

        # Check for page_size
        if 'page_size' in payload and payload['page_size'] != "":
            page_size = payload['page_size']

        if not from_cached:
            self.cache_manager.register_cache_state_keys()
            # 3. set cache data for the grid
            data = self.get_data(request, *args, **kwargs)
            data = data['data']
            fields = data['fields']
            self.cache_manager.set_grid_cache_data(data=data, fields=fields)
            # 4. Get the data from the cache manager
            data = self.cache_manager.get_data()
        page = self.paginate_queryset(data)
        return self.paginator.get_paginated_response(page)
