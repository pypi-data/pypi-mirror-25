# -*- coding: utf-8 -*-
"""Post install import steps for ps.plone.mlstiles."""

# python imports
import pkg_resources

# zope imports
from Products.CMFPlone.interfaces import INonInstallable
from Products.GenericSetup.interfaces import IProfileImportedEvent
from plone import api
from zope.component import adapter
from zope.interface import implementer

# local imports
from ps.plone.mlstiles import config


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Define hidden GenericSetup profiles."""

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ps.plone.mlstiles:support_cover',
            'ps.plone.mlstiles:support_mosaic',
            'ps.plone.mlstiles:uninstall',
        ]


@adapter(IProfileImportedEvent)
def handle_profile_imported_event(event):
    """Update 'last version for profile' after a full import."""
    qi = api.portal.get_tool(name='portal_quickinstaller')
    setup = api.portal.get_tool(name='portal_setup')

    if not qi.isProductInstalled(config.PROJECT_NAME):
        return

    if event.profile_id == 'profile-plone.app.upgrade.v50:to50alpha3':
        setup.runAllImportStepsFromProfile(config.INSTALL_PROFILE)

    if event.profile_id == 'profile-plone.app.mosaic:default':
        setup.runAllImportStepsFromProfile(config.MOSAIC_SUPPORT_PROFILE)

    if event.profile_id == 'profile-collective.cover:default':
        setup.runAllImportStepsFromProfile(config.COVER_SUPPORT_PROFILE)


def install_additional_profiles(context):
    """Install additional support profiles."""
    if not context.readDataFile('ps.plone.mlstiles.txt'):
        return

    qi = api.portal.get_tool(name='portal_quickinstaller')
    setup = api.portal.get_tool(name='portal_setup')

    if qi.isProductInstalled('collective.cover'):
        setup.runAllImportStepsFromProfile(config.COVER_SUPPORT_PROFILE)

    if qi.isProductInstalled('plone.app.mosaic'):
        setup.runAllImportStepsFromProfile(config.MOSAIC_SUPPORT_PROFILE)


def install_cover_support(context):
    """Register tiles collective.cover."""
    if not context.readDataFile('ps.plone.mlstiles.cover.txt'):
        return

    try:
        pkg_resources.get_distribution('collective.cover')
    except pkg_resources.DistributionNotFound:
        return

    tiles = [
        u'ps.plone.mlstiles.developments.collection',
        u'ps.plone.mlstiles.listings.collection',
        u'ps.plone.mlstiles.listings.recent',
        u'ps.plone.mlstiles.listings.featured',
        u'ps.plone.mlstiles.listings.search',
    ]
    calendar_tile = u'collective.cover.calendar'

    from collective.cover.controlpanel import ICoverSettings
    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    try:
        available_tiles.remove(calendar_tile)
    except ValueError:
        pass  # no calendar tile found
    for tile in tiles:
        if tile not in available_tiles:
            available_tiles.append(tile)

    api.portal.set_registry_record(value=available_tiles, **record)
