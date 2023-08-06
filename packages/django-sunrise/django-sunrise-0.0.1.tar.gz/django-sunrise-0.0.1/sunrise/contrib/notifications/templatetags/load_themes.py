from django import template
from django.template.loader import get_template
from sunrise.contrib.notifications.models import UserTheme, UserPreferences

register = template.Library()

def themes(user):
    
    username = user.username
    #Get Preferences
    prefObj = UserPreferences.objects.filter(username = username)
    if len(prefObj) > 0:
        active = prefObj[0].data['theme']
    else:
        active = 'Watermelon'
    all_themes = UserTheme.objects.all()
    themes = all_themes.filter(name = active)
    if len(themes) > 0:
        _link = themes[0].data['link']
    else:
        try:
            _link = all_themes[0].data['link']
        except:
            _link = ""
    return {'link': _link}


t = get_template('themes.html')
register.inclusion_tag(t)(themes)