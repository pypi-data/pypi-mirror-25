"""
Plugs Status Settings
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

MANDATORY_SETTINGS = ['ENGINE']
DATABASE_SETTINGS = getattr(settings, 'DATABASES', {})
PROJECT_SETTINGS = DATABASE_SETTINGS.get('default', {})

for setting in MANDATORY_SETTINGS:
    try:
        PROJECT_SETTINGS[setting]
    except KeyError:
        raise ImproperlyConfigured('Missing setting: DATABASES[\'default\'][\'{0}\']'.format(setting))

PROJECT_SETTINGS['NAME'] = PROJECT_SETTINGS.get('NAME', None)
PROJECT_SETTINGS['USER'] = PROJECT_SETTINGS.get('USER', None)
PROJECT_SETTINGS['PASSWORD'] = PROJECT_SETTINGS.get('PASSWORD', None)
PROJECT_SETTINGS['HOST'] = PROJECT_SETTINGS.get('HOST', None)
PROJECT_SETTINGS['PORT'] = PROJECT_SETTINGS.get('PORT', None)

app_settings = PROJECT_SETTINGS
