# Author: Integra
# Dev: Partha(Ref)
from datetime import datetime

from sunrise.restful.viewsets import ViewSetManager as SunriseModelViewSet

from .serializers import MenuStructureSerializer, AddonSerializer, AddonHistorySerializer
from .models import MenuStructure, Addon, AddonHistory


class MenuStructureViewset(SunriseModelViewSet):
    model = MenuStructure
    parser = {
        'default':MenuStructureSerializer
    }

class AddonViewSet(SunriseModelViewSet):
    model = Addon
    parser = {
        'default':AddonSerializer
    }


    def post_save(self, request, instance, created, data=None):
        if 'status' in data.keys():
            activity = AddonHistory()
            activity.addon =  instance
            activity.audit_user = request.user.username            
            activity.data = {
                'message': '%s <b>%s</b> %s on %s'%(request.user.username,instance.status, instance.name, datetime.now().strftime("%m-%d-%Y %H:%M:%S %p")),
                'user': request.user.username,
                'status': instance.status,
                'addon': instance.name,
                'on': datetime.now().strftime("%m-%d-%Y %H:%M:%S %p")
            }
            activity.save()
        return instance


class AddonHistoryViewSet(SunriseModelViewSet):
    model = AddonHistory
    parent = Addon

    parser = {
        'default':AddonHistorySerializer
    }

    