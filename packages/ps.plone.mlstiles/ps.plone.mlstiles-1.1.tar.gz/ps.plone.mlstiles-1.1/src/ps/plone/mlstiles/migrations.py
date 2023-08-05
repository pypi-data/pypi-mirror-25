# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.mlstiles."""

# zope imports
from plone import api

# local imports
from ps.plone.mlstiles import config


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Install ps.plone.mls
    * Add featured listings tile.
    """
    setup = api.portal.get_tool(name='portal_setup')
    qi = api.portal.get_tool(name='portal_quickinstaller')

    qi.installProduct('ps.plone.mls')
    setup.runImportStepFromProfile(
        config.INSTALL_PROFILE,
        'plone.app.registry',
    )


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * Add development collection tile.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(
        config.INSTALL_PROFILE,
        'plone.app.registry',
    )


def migrate_to_1003(context):
    """Migrate from 1002 to 1003.

    * Add browserlayer.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(config.INSTALL_PROFILE, 'browserlayer')


def migrate_to_1004(context):
    """Migrate from 1003 to 1004.

    * Add browserlayer.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runAllImportStepsFromProfile(config.INSTALL_PROFILE)


def migrate_to_3002(context):
    """Migrate from 3001 to 3002.

    * Add listing search results tile.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(config.MOSAIC_SUPPORT_PROFILE, 'registry')
