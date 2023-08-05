# -*- coding: utf-8
import logging
import os
import sys
import importlib
from django.apps import AppConfig
from django.conf import settings
from dj_n3_templateplugins.plugin import TemplatePlugin
from dj_n3_templateplugins.utils import get_plugin_class


LOGGER = logging.getLogger(__name__)
PLUGIN_DIR = getattr(settings, 'N3PLUGINS_PLUGIN_DIR', 'plugins')


class DjN3TemplatepluginsConfig(AppConfig):
    name = 'dj_n3_templateplugins'

    def ready(self):
        super().ready()
        self.load_plugins()

    def load_plugins(self):
        from .models import Plugin
        LOGGER.debug('loading plugins')
        directory = os.listdir(PLUGIN_DIR)
        LOGGER.debug('checking plugin_dir %s', PLUGIN_DIR)
        for f in directory:
            path = os.path.join(PLUGIN_DIR, f)
            if os.path.isdir(path):
                LOGGER.debug('loading plugin %s', f)
                #todo: Cleaner way to do this.  I'd like to use utils.get_plugin_class() but since this is validation
                #todo: we don't have an instance in our DB yet.  This violates DRY.
                sys.path.append(PLUGIN_DIR)
                pmod = importlib.import_module(name=f)
                sys.path.pop()

                if self.validate_plugin(pmod.Plugin):
                    plugin, created = Plugin.objects.get_or_create(name=f, defaults={
                        'pythonpath': '/'.join(PLUGIN_DIR, f)
                    })
                    LOGGER.info('get_or_create, created: %s, plugin: %s:%s', created, plugin.name, plugin.status)
                else:
                    LOGGER.warning('Plugin must be a valid plugin, did you inherit from plugin.TemplatePlugin?')

    @staticmethod
    def validate_plugin(cls):
        """Validate that the given class is a proper dj_n3_templateplugin

        Args:
            cls (Class):  the plugin class to be loaded

        Returns:
            bool: True if valid, False if not.

        """
        return isinstance(cls(), TemplatePlugin)

