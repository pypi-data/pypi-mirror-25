""" Used to render the mode to the template """
# Author: Partha


from django.conf import settings
from sunrise.contrib.authentication.models import (PageGroup, RolePageAccess,
                                                   SunriseProfile)


def mode_details(request):
    """ Used to send the page type """
    try:
        parts = request.path.strip('/').split('/')
        url = ('/%s/' % ('/'.join(parts[0:2])))
        data = request.path.split("/")
        profile = SunriseProfile.objects.get(username=request.user.username)
        roles_assigned = profile.roles.all()
        roles = RolePageAccess.objects.filter(
            role__in=roles_assigned, role__status='Active', page__url=url)
        page_category = PageGroup.objects.filter(url=url)[0].page_category
        access_type = ''
        if roles.count() > 0:
            access_types = list(
                set(roles.values_list('access_type', flat=True)))
            if 'U' in access_types:
                access_type = 'U'
            else:
                access_type = 'R'
        return {
            'app': data[1],
            'prefix': data[2],
            'mode': data[3],
            'access_type': access_type,
            'page_category': page_category
        }
    except Exception, general_exception:
        return {
            'app': "",
            'prefix': "",
            'mode': "",
            'access_type': ""
        }
