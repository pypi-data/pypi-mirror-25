"""Decorators for django-n3-templateplugins"""
import importlib
import sys
from django.conf import settings
from dj_n3_templateplugins.models import Plugin
from dj_n3_templateplugins.utils import get_plugin_instance

PLUGIN_DIR = getattr(settings, 'N3PLUGINS_PLUGIN_DIR', 'plugins')


def load_plugins(cls):
    cls.plugins = {}
    for plugin in Plugin.objects.filter(status=0):
        p = get_plugin_instance(plugin)
        cls.plugins[plugin.name] = {'plugin_object': plugin, 'instance': p, 'context': p.get_context_data()}
    return cls
