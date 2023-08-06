# -*- coding: utf-8 -*-
from zope.interface import Interface

PLUGIN_NAME = 'genericsetup'

DEFAULT_ENABLED_PROFILE_NAME = 'install'
DEFAULT_DISABLED_PROFILE_NAME = 'uninstall'
DEFAULT_ENABLED_LOCALES_NAME = 'locales'
DEFAULT_ENABLED_MODELS_NAME = 'models'
DEFAULT_ENABLED_RESOURCES_NAME = 'resources'

NO = ['off', 'false', 'no', '0']
YES = ['on', 'true', 'yes', '1']


class IGenericSetupExportableContainer(Interface):
    """Marker interface for exportable content"""
