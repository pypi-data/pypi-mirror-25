# Author: Integra
# Dev: Partha
# Desc: This is used to specify the Custom Permission Classes

from rest_framework import permissions
from sunrise.contrib.oauth.models import AppResourcePermission


class AdminCheckPermission(permissions.BasePermission):
    """
    Global permission check for admin.
    """

    def has_permission(self, request, view):
        """ base method to check the permission """
        if request.user.is_superuser:
            return True
        else:
            return False


class OAuthPermission(permissions.BasePermission):
    """This is used to check if the request comes from OAuth then particual
    resource have permission or not """

    def has_permission(self, request, view):
        """ base method to check the permission """
        if request.user is not None and request.user.is_authenticated():
            return True
        else:
            if request.auth is None:
                return False
        try:
            _path = request.path.split("/")
            base_path = ""
            for item in _path[:4]:
                base_path = base_path + item + "/"
            _perm = AppResourcePermission.objects.get(
                appID=request.auth.application, api_url=base_path)
        except AppResourcePermission.DoesNotExist:
            return False

        if view.action == "list":
            return _perm.can_list
        if view.action == "retrieve":
            return _perm.can_retrieve
        if view.action == "create":
            return _perm.can_create
        if view.action == "update":
            return _perm.can_update
        if view.action == "destroy":
            return _perm.can_destroy
