# Author: Integra
# Dev: Partha.K

from sunrise.restful.serializers import NormalSerializer

from .models import QueryManager
from .models import RequestQueryViewer

class QueryManagerSerializer(NormalSerializer):
    class Meta:
        model = QueryManager


class RequestQueryViewerSerializer(NormalSerializer):
	class Meta:
		model = RequestQueryViewer