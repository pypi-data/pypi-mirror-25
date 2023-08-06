""" Base module for page """
# Author: partha

import json

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.generic import View


def get_all_subclasses(klass):
    """ Used to return the subclasses of a class """
    all_subclasses = []
    for subclass in klass.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses


class BaseView(View):
    """ Class based view to resolve the functionality routes based on the request path """
    template = None
    _accepted_views = ['search', 'add', 'view']

    def __init__(self, **kwargs):
        """ Getting template name """
        self.template = kwargs['template']
        del kwargs['template']
        self.initiate()
        # Check for the plugin here
        plugins = get_all_subclasses(self.__class__)
        if len(plugins) > 0:
            self.__class__ = plugins[-1]
        super(BaseView, self).__init__(**kwargs)

    def initiate(self):
        """ For any common initiation """
        pass

    def mutate_request(self, request):
        """ Mutating the Request Contents """
        setattr(request, 'POST', request.POST.copy())
        setattr(request, 'GET', request.GET.copy())
        return request

    def get(self, request, dispatch=None):
        """ Invoked wheh the request type is GET """
        if dispatch in self._accepted_views:
            return getattr(self, dispatch)(request)
        else:
            if hasattr(self, dispatch):
                return getattr(self, dispatch)(request)
        raise Http404("Page Not Found")

    def post(self, request, dispatch=None):
        """ Invoked wheh the request type is GET """
        if dispatch in ['save', 'update']:
            return getattr(self, dispatch)(request)
        else:
            if hasattr(self, dispatch):
                return getattr(self, dispatch)(request)
        raise Http404("Page Not Found")


class PageView(BaseView):
    """ Basic PageView for SAVE type pages """

    def search(self, request):
        """ Invoked when the request URL contains the /search/ in the path """
        context = {}

        if hasattr(self, 'ADD'):
            context.update({'ADD': self.ADD})
        else:
            context.update({'ADD': True})
        return render(request, self.template, context)

    def add(self, request):
        """ Invoked when the request URL contains the /add/ in the path """
        return render(request, self.template, {})

    def view(self, request):
        """ Invoked wheh the request URL contains the /view/ in the path """
        return render(request, self.template, {})

    def get_parent_model(self, request, model):
        """ Will return parent model for the specified model """
        return [
            (f, f.name if f.model != model else f.name)
            for f in model._meta.get_fields()
            if (
                f.one_to_one
                or (f.many_to_one and f.related_model)
            )
        ]


class SearchAddView(PageView):
    """ Search/Add/View/Edit """

    def get_model_instance(self, modelname):
        """ This is used to get the model instance of the given modelname """
        all_models = apps.get_models()
        for every_model in all_models:
            if modelname == every_model._meta.object_name:
                return every_model
        return None

    def get_related_fkey(
            self,
            parent,
            child
    ):
        """ will return the fkey between 2 models """
        fkey = None
        for field in self.get_model_instance(child.model._meta.object_name)._meta.fields:
            if (field.get_internal_type() == "ForeignKey" or
                    field.get_internal_type() == "OneToOneField"):
                if field.rel.to.__name__ == parent.model._meta.object_name:
                    fkey = field.name
                    break
        return fkey

    def set_prestine(
            self,
            childs,
            request,
            action,
            pk_container=None
    ):
        """ Used to restore the cache state """
        for child in childs:
            child_type = child[1]
            if child_type == 'grid':
                grid_key = child[2]
                child_viewset = child[0]()
                setattr(child_viewset, 'action', action)
                setattr(child_viewset, 'request', request)
                child_viewset._initiate_cache_manager(grid_key=grid_key)
                child_viewset.cache_manager.setStableState(
                    pk_container[grid_key])
        return True

    def save(
            self,
            *args,
            **kwargs
    ):
        """ Saving parents and child atomic """
        pk_container = {}
        try:
            with transaction.atomic():
                # Check for the Active plugins for this plage
                parent_data = json.loads(self.request.POST['header'])
                if 'details' in self.request.POST.keys():
                    child_data = json.loads(self.request.POST['details'])
                else:
                    child_data = None
                parent_saved = False
                # 1. Get parent viewset
                parent_viewset = self.parent()
                setattr(parent_viewset, 'action', 'create')
                setattr(parent_viewset, 'request', self.request)
                if hasattr(parent_viewset, 'populate'):
                    parent_data = parent_viewset.populate(
                        self.request, parent_data, 'create')
                serializer = parent_viewset.get_serializer(
                    data=parent_data)
                if serializer.is_valid():
                    parent_instance = serializer.save()
                    if hasattr(parent_viewset, 'post_save'):
                        parent_viewset.post_save(
                            self.request, parent_instance, created=True, data=parent_data)
                    parent_saved = True
                else:
                    raise ValidationError(serializer.errors)
                # 2. Save childs data
                if parent_saved:
                    # 3. Get childs viwset instance
                    for child in self.childs:
                        child_viewset = child[0]()
                        setattr(child_viewset, 'action', 'create')
                        setattr(child_viewset, 'request', self.request)
                        # Get child type
                        child_type = child[1]
                        # Get prefix
                        child_prefix = child[2]
                        fkey = self.get_related_fkey(
                            parent_viewset, child_viewset)

                        if child_type == "normal":
                            # Nothing but a normal child
                            # get fkey
                            if fkey is not None:
                                child_data[child_prefix].update(
                                    {fkey: parent_instance.pk})
                                if hasattr(child_viewset, 'populate'):
                                    child_data[child_prefix] = child_viewset.populate(
                                        self.request, child_data[child_prefix], 'create')
                                serializer = child_viewset.get_serializer(
                                    data=child_data[child_prefix])
                                if serializer.is_valid():
                                    child_object = serializer.save()
                                    if hasattr(child_viewset, 'post_save'):
                                        child_viewset.post_save(
                                            self.request,
                                            child_object,
                                            created=True,
                                            data=child_data[child_prefix]
                                        )
                                else:
                                    raise ValidationError(serializer.errors)

                        if child_type == "grid":
                            # Get cache key
                            try:
                                grid_key = self.request.META['HTTP_X_GRIDKEY']
                            except Exception, general_exception:
                                grid_key = child[2]
                            pk_container.update({grid_key: {}})
                            child_viewset._initiate_cache_manager(
                                grid_key=grid_key)
                            # 2. Get items to delete
                            items_to_delete = child_viewset.cache_manager.items_to_delete
                            # 3. Get items to update
                            items_to_update = child_viewset.cache_manager.items_to_update
                            # 4. Get items to add
                            items_to_add = child_viewset.cache_manager.items_to_add
                            # 5. deleting all items_to_delete
                            for item in items_to_delete:
                                # need to get pk field dynamically
                                if "id" in item and item['id'] != "":
                                    to_be_deleted = child_viewset.model.objects.get(
                                        pk=item['id'])  # need to improve no of hits
                                    to_be_deleted.delete()
                            # 6. Update all items in items_to_update
                            for item in items_to_update:
                                if "id" in item:
                                    # Remove the material keys
                                    material_keys = [
                                        "row_bound_status", "row_added_status", "grid_index"]
                                    temp = [item.pop(key, None)
                                            for key in material_keys]
                                    #Validating and updating
                                    partial = kwargs.pop('partial', True)
                                    instance = child_viewset.model.objects.get(
                                        pk=item['id'])

                                    data = {}
                                    for key, val in item.items():
                                        if val is not None:
                                            if isinstance(val, tuple) is True and val[1] == 'unbound':
                                                data.update({key: val[0]})
                                    data.update({fkey: parent_instance.pk})
                                    if hasattr(child_viewset, 'populate'):
                                        data = child_viewset.populate(
                                            child_viewset.request, data, 'update')
                                    serializer = child_viewset.get_serializer(
                                        instance, data=data, partial=True)
                                    if serializer.is_valid():
                                        child_viewset.perform_update(
                                            serializer)
                                        if hasattr(child_viewset, 'post_save'):
                                            child_viewset.post_save(
                                                self.request, instance, created=False, data=data)
                                    else:
                                        _errors = serializer.errors
                                        _errors.update({'at_row': temp[2]})
                                        raise ValidationError(_errors)
                            # 7. Add all items in items_to_add
                            for item in items_to_add:
                                material_keys = [
                                    "row_bound_status", "row_added_status", "grid_index"]
                                temp = [item.pop(key, None)
                                        for key in material_keys]
                                data = {}
                                for key, val in item.items():
                                    if val is not None and isinstance(val, tuple) is True:
                                        data.update({key: val[0]})
                                data.update({fkey: parent_instance.pk})
                                if hasattr(child_viewset, 'populate'):
                                    data = child_viewset.populate(
                                        child_viewset.request, data, 'create')
                                serializer = child_viewset.get_serializer(
                                    data=data)
                                if serializer.is_valid():
                                    child_viewset.object = serializer.save()
                                    pk_container[grid_key].update(
                                        {temp[2]: child_viewset.object.pk})
                                    if hasattr(child_viewset, 'post_save'):
                                        child_viewset.post_save(
                                            self.request, child_viewset.object, created=True, data=data)
                                else:
                                    _errors = serializer.errors
                                    _errors.update({'at_row': temp[2]})
                                    raise ValidationError(_errors)
                    # 8. Removing cache contents of modified, deleted
                    self.set_prestine(self.childs, self.request,
                                     'create', pk_container)
        except Exception, general_exception:
            try:
                to_return = json.dumps(general_exception.message_dict)
            except Exception, invalid_json:
                to_return = str(general_exception)
            return HttpResponse(to_return, status=400)
        return HttpResponse(json.dumps({'status': 'records saved successfully', 'parent_pk': parent_instance.pk}))

    def update(self, *args, **kwargs):
        """ Saving parents and child atomic """
        pk_container = {}
        try:
            with transaction.atomic():
                parent_data = json.loads(self.request.POST['header'])
                if 'details' in self.request.POST.keys():
                    child_data = json.loads(self.request.POST['details'])
                else:
                    child_data = None
                parent_saved = False
                # 1. Get parent viewset
                # check for the plugin
                parent_viewset = self.parent()  # Get it from the subclass
                setattr(parent_viewset, 'action', 'update')
                setattr(parent_viewset, 'request', self.request)
                partial = kwargs.pop('partial', False)
                # get pk data
                try:
                    _parent_pk = parent_data[parent_viewset.lookup_field]
                except Exception, general_exception:
                    if parent_viewset.lookup_url_kwarg is not None:
                        try:
                            _parent_pk = int(
                                parent_data[parent_viewset.lookup_url_kwarg])
                        except Exception, general_exception:
                            _parent_pk = int(parent_data['id'])
                    else:
                        _parent_pk = int(parent_data['id'])

                parent_instance = parent_viewset.get_object(
                    pk=_parent_pk)
                previous_data = parent_instance.__dict__
                for key, val in previous_data.items():
                    if key in parent_data.keys():
                        if previous_data[key] == parent_data[key]:
                            parent_data.pop(key, None)
                if hasattr(parent_viewset, 'populate'):
                    parent_data = parent_viewset.populate(
                        self.request, parent_data, 'update')
                serializer = parent_viewset.get_serializer(
                    parent_instance, data=parent_data, partial=True)

                if serializer.is_valid():
                    result = parent_viewset.perform_update(serializer)
                else:
                    raise ValidationError(serializer.errors)
                if hasattr(parent_viewset, 'post_save'):
                    parent_instance = parent_viewset.post_save(
                        self.request, parent_instance, created=False, data=parent_data)
                parent_saved = True
                # if child_data is None:
                #     return HttpResponse({'status':'Record Saved Successfully'})
                # 2. Save childs data
                if parent_saved:
                    # 3. Get childs viwset instance
                    from_childs = self.childs
                    for child in from_childs:
                        # Get it from subclass
                        child_viewset = child[0]()
                        setattr(child_viewset, 'action', 'update')
                        setattr(child_viewset, 'request', self.request)
                        # Get child type
                        child_type = child[1]
                        # Get prefix
                        child_prefix = child[2]
                        fkey = self.get_related_fkey(
                            parent_viewset, child_viewset)
                        if fkey is not None:
                            fkey = fkey
                        if child_type == "normal":
                            # Nothing but a normal child
                            # get fkey

                            fkey = self.get_related_fkey(
                                parent_viewset, child_viewset)
                            if fkey is not None:
                                # fkey = fkey + "_id"
                                child_data[child_prefix].update(
                                    {fkey: parent_instance.pk})
                                instance = child_viewset.model.objects.get(
                                    pk=child_data[child_prefix]['id'])
                                previous_data = instance.__dict__
                                for key, val in previous_data.items():
                                    if key in child_data[child_prefix].keys():
                                        if previous_data[key] == child_data[child_prefix][key]:
                                            child_data[child_prefix].pop(
                                                key, None)

                                serializer = child_viewset.get_serializer(
                                    instance, data=child_data[child_prefix], partial=True)
                                if serializer.is_valid():
                                    child_object = serializer.save()
                                    if hasattr(child_viewset, 'post_save'):
                                        child_viewset.post_save(
                                            self.request, child_object, created=True, data=child_data[child_prefix])
                                else:
                                    raise ValidationError(serializer.errors)
                        if child_type == "grid":
                            # Get cache key
                            try:
                                grid_key = self.request.META['HTTP_X_GRIDKEY']
                            except Exception, general_exception:
                                grid_key = child[2]
                            pk_container.update({grid_key: {}})

                            child_viewset._initiate_cache_manager(
                                grid_key=grid_key
                            )
                            # 2. Get items to delete
                            items_to_delete = child_viewset.cache_manager.items_to_delete
                            # 3. Get items to update
                            items_to_update = child_viewset.cache_manager.items_to_update
                            # 4. Get items to add
                            items_to_add = child_viewset.cache_manager.items_to_add

                            # 5. deleting all items_to_delete
                            for item in items_to_delete:
                                # need to get pk field dynamically
                                if "id" in item and item['id'] != "":
                                    to_be_deleted = child_viewset.model.objects.get(
                                        pk=item['id'])  # need to improve no of hits
                                    to_be_deleted.delete()
                            # 6. Update all items in items_to_update
                            for item in items_to_update:
                                if "id" in item:
                                    # Remove the material keys
                                    material_keys = [
                                        "row_bound_status", "row_added_status", "grid_index"]
                                    temp = [item.pop(key, None)
                                            for key in material_keys]
                                    #Validating and updating
                                    partial = kwargs.pop('partial', False)
                                    instance = child_viewset.model.objects.get(
                                        pk=item['id'][0])
                                    data = {}
                                    for key, val in item.items():
                                        if val is not None:
                                            if isinstance(val, tuple) is True and val[1] == 'unbound':
                                                data.update({key: val[0]})
                                    data.update({fkey: parent_instance.pk})
                                    if hasattr(child_viewset, 'populate'):
                                        data = child_viewset.populate(
                                            child_viewset.request, data, 'update')
                                    serializer = child_viewset.get_serializer(
                                        instance, data=data, partial=True)
                                    if serializer.is_valid():
                                        child_viewset.perform_update(
                                            serializer)
                                        if hasattr(child_viewset, 'post_save'):
                                            child_viewset.post_save(
                                                self.request, instance, created=False, data=data)
                                    else:
                                        _errors = serializer.errors
                                        _errors.update({'at_row': temp[2]})
                                        raise ValidationError(_errors)
                            # 7. Add all items in items_to_add
                            for item in items_to_add:
                                material_keys = [
                                    "row_bound_status", "row_added_status", "grid_index"]
                                temp = [item.pop(key, None)
                                        for key in material_keys]
                                data = {}
                                for key, val in item.items():
                                    if val is not None and isinstance(val, tuple):
                                        data.update({key: val[0]})
                                data.update({fkey: parent_instance.pk})
                                if hasattr(child_viewset, 'populate'):
                                    data = child_viewset.populate(
                                        child_viewset.request, data, 'create')
                                serializer = child_viewset.get_serializer(
                                    data=data)
                                if serializer.is_valid():
                                    child_viewset.object = serializer.save()
                                    pk_container[grid_key].update(
                                        {temp[2]: child_viewset.object.pk})
                                    if hasattr(child_viewset, 'post_save'):
                                        child_viewset.post_save(
                                            self.request, child_viewset.object, created=False, data=data)
                                else:
                                    _errors = serializer.errors
                                    _errors.update({'at_row': temp[2]})
                                    raise ValidationError(_errors)
                    # 8. Removing cache contents of modified, deleted
                    self.set_prestine(self.childs, self.request,
                                      'update', pk_container)
        except Exception, general_exception:
            try:
                to_return = json.dumps(general_exception.message_dict)
            except Exception, json_exception:
                to_return = str(e)
            return HttpResponse(to_return, status=400)
        return HttpResponse(json.dumps({'status': 'records saved successfully', 'parent_pk': parent_instance.pk}))


class SearchView(PageView):
    """ second category pages """
    def set_prestine(
            self,
            childs,
            request,
            action,
            pk_container=None
    ):
        """ Used to restore to the original state """
        for child in childs:
            grid_key = child[1]
            child_viewset = child[0]()
            setattr(child_viewset, 'action', action)
            setattr(child_viewset, 'request', request)
            child_viewset._initiate_cache_manager(grid_key=grid_key)
            child_viewset.cache_manager.setStableState(
                pk_container[grid_key])
        return True

    def update(
            self,
            *args,
            **kwargs
    ):
        """ Updating all childs atomoicly """
        pk_container = {}
        try:
            with transaction.atomic():
                for child in self.childs:
                    parent = child
                    grid_key = parent[1]
                    pk_container.update({grid_key: {}})
                    child_viewset = parent[0]()
                    setattr(child_viewset, 'action', 'update')
                    setattr(child_viewset, 'request', self.request)
                    child_viewset._initiate_cache_manager(
                        grid_key=grid_key)
                    # 2. Get items to delete
                    items_to_delete = child_viewset.cache_manager.items_to_delete
                    # 3. Get items to update
                    items_to_update = child_viewset.cache_manager.items_to_update
                    # 4. Get items to add
                    items_to_add = child_viewset.cache_manager.items_to_add

                    # 5. deleting all items_to_delete
                    for item in items_to_delete:
                        # need to get pk field dynamically
                        if "id" in item and item['id'] != "":
                            to_be_deleted = child_viewset.model.objects.get(
                                pk=item['id'])  # need to improve no of hits
                            to_be_deleted.delete()
                    # 6. Update all items in items_to_update
                    for item in items_to_update:
                        if "id" in item:
                            # Remove the material keys
                            material_keys = ["row_bound_status",
                                             "row_added_status", "grid_index"]
                            temp = [item.pop(key, None)
                                    for key in material_keys]
                            #Validating and updating
                            partial = kwargs.pop('partial', False)
                            instance = child_viewset.model.objects.get(
                                pk=item['id'][0])
                            data = {}
                            for key, val in item.items():
                                if val is not None:
                                    if isinstance(val, tuple) and val[1] == 'unbound':
                                        data.update({key: val[0]})
                            if hasattr(child_viewset, 'populate'):
                                data = child_viewset.populate(
                                    child_viewset.request, data, 'update')
                            serializer = child_viewset.get_serializer(
                                instance, data=data, partial=True)
                            if serializer.is_valid():
                                child_viewset.perform_update(serializer)
                                if hasattr(child_viewset, 'post_save'):
                                    child_viewset.post_save(
                                        self.request, instance, created=False, data=data)
                            else:
                                _errors = serializer.errors
                                _errors.update({'at_row': temp[2]})
                                raise ValidationError(_errors)
                    # 7. Add all items in items_to_add
                    for item in items_to_add:
                        material_keys = ["row_bound_status",
                                         "row_added_status", "grid_index"]
                        temp = [item.pop(key, None) for key in material_keys]
                        data = {}
                        for key, val in item.items():
                            if val is not None and isinstance(val, tuple):
                                data.update({key: val[0]})
                        if hasattr(child_viewset, 'populate'):
                            data = child_viewset.populate(
                                child_viewset.request, data, 'create')
                        serializer = child_viewset.get_serializer(
                            data=data)
                        if serializer.is_valid():
                            child_viewset.object = serializer.save()
                            pk_container[grid_key].update(
                                {temp[2]: child_viewset.object.pk})
                            if hasattr(child_viewset, 'post_save'):
                                child_viewset.post_save(
                                    self.request, child_viewset.object, created=False, data=data)
                        else:
                            _errors = serializer.errors
                            _errors.update({'at_row': temp[2]})
                            raise ValidationError(_errors)
                # 8. Removing cache contents of modified, deleted
                self.set_prestine(self.childs, self.request,
                                  'update', pk_container)
        except Exception, general_exception:
            try:
                to_return = json.dumps(general_exception.message_dict)
            except Exception, json_exception:
                to_return = str(general_exception)
            return HttpResponse(to_return, status=400)
        return HttpResponse(json.dumps({'status': 'records saved successfully'}))
