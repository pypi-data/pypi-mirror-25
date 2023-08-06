# -*- coding: UTF-8 -*-
import six
from django.test.signals import setting_changed
from django.conf import settings
from importlib import import_module
DEFAULTS = {
    'MODEL': None,
    'TABLE': None,
}

IMPORT_STRINGS = (
    'MODEL',
    'TABLE',
)

REMOVED_SETTINGS = ()

def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val

def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class HTMLClientDejaVuSettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:
        from rest_framework.settings import db_settings
        print(db_settings.DEFAULT_RENDERER_CLASSES)
    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'HTMLCLIENTDEJAVU', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "http://www.django-rest-framework.org/api-guide/settings/"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings." % (
                    setting, SETTINGS_DOC))
        return user_settings


dejavu_settings = HTMLClientDejaVuSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_db_settings(*args, **kwargs):
    global dejavu_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'HTMLCLIENTDEJAVU':
        dejavu_settings = HTMLClientDejaVuSettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_db_settings)