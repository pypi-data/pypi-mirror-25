# Author: Integra
# Dev: Partha(Ref)

from rest_framework.filters import BaseFilterBackend

class SunriseFilterBackend(BaseFilterBackend):
    """ Basic filter backend """
    def filter_queryset(
            self,
            request,
            queryset,
            view
    ):
        """ basic filter """
        filter_fields = getattr(view, 'filter_fields', None)

        if filter_fields:
            return view.filtering(request.query_params, 
            		queryset = queryset, 
            		user = request.user)
        return queryset
