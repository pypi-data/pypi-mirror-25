# Author: Integra
# Dev: Partha(Ref)

from rest_framework import serializers as baseserializer
from rest_framework_hstore.fields import HStoreField

from sunrise.restful import serializers
from sunrise.restful.serializers import NormalSerializer
from .models import MenuStructure, Addon, AddonHistory

class MenuStructureSerializer(NormalSerializer):
    data = HStoreField()
    class Meta:
        model = MenuStructure

class AddonSerializer(NormalSerializer):
    class Meta:
        model = Addon

class AddonHistorySerializer(NormalSerializer):
    class Meta:
        model = AddonHistory
