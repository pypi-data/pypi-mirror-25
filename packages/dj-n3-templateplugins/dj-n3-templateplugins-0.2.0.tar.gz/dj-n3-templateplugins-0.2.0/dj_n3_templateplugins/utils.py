""" Common utilities for django-n3-templateplugins"""

import importlib
import sys
from django.conf import settings
from dj_n3_templateplugins.models import Plugin

PLUGIN_DIR = getattr(settings, 'N3PLUGINS_PLUGIN_DIR', 'plugins')


def get_plugin_instance(plugin_object):
    """returns an instance of a plugin, given an entry from our database (Plugin)

    Args:
        plugin_object (Plugin): Instance of the Django Plugin Module (aka one of our registered plugins from the db)

    Returns:
        class: An instance of the given plugin
    """
    Plugin = get_plugin_class(plugin_object)
    return Plugin()


def get_plugin_class(plugin_object):
    """returns the class of a plugin, given an entry from our database (Plugin)

    Args:
        plugin_object (Plugin): Instance of the Django Plugin Module (aka one of our registered plugins from the db)

    Returns:
        class: The actual class (not an instance of it)
    """
    sys.path.append(PLUGIN_DIR)
    pmod = importlib.import_module(name=plugin_object.name)
    sys.path.pop()
    return pmod.Plugin
