# -*- coding: utf-8 -*-
"""Test Layer for ps.plone.mlstiles."""

# python imports
import pkg_resources
import unittest

# zope imports
try:
    from collective.cover.tests.utils import create_standard_content_for_tests
    HAS_COVER = True
except ImportError:
    HAS_COVER = False
try:
    import plone.app.mosaic  # noqa
    HAS_MOSAIC = True
except ImportError:
    HAS_MOSAIC = False
from plone.app.testing import (
    IntegrationTesting,
    PloneSandboxLayer,
    PLONE_FIXTURE,
)

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PA_CONTENTTYPES = False
else:
    HAS_PA_CONTENTTYPES = True


def skip_if_no_cover(testfunc):
    """Skip test if collective.cover is missing."""
    try:
        import collective.cover  # noqa
    except ImportError:
        return unittest.skip('collective.cover is not installed')(testfunc)
    else:
        return testfunc


def skip_if_no_mosaic(testfunc):
    """Skip test if plone.app.mosaic is missing."""
    try:
        import plone.app.mosaic  # noqa
    except ImportError:
        return unittest.skip('plone.app.mosaic is not installed')(testfunc)
    else:
        return testfunc


class PSPloneMLSTiles(PloneSandboxLayer):
    """Custom Test Layer for ps.plone.mlstiles."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)

        if HAS_PA_CONTENTTYPES:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)

        if HAS_COVER:
            import collective.cover
            self.loadZCML(package=collective.cover)

        if HAS_MOSAIC:
            self.loadZCML(package=plone.app.mosaic)

        import ps.plone.mlstiles
        self.loadZCML(package=ps.plone.mlstiles)

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        # Plone 5 support
        if HAS_PA_CONTENTTYPES:
            self.applyProfile(portal, 'plone.app.contenttypes:default')

        self.applyProfile(portal, 'ps.plone.mlstiles:default')
        self.applyProfile(portal, 'ps.plone.mls:testfixture')

        if HAS_COVER:
            # setup test content
            self.applyProfile(portal, 'collective.cover:default')
            self.applyProfile(portal, 'collective.cover:testfixture')
            self.applyProfile(portal, 'ps.plone.mlstiles:support_cover')
            create_standard_content_for_tests(portal)

        if HAS_MOSAIC:
            self.applyProfile(portal, 'plone.app.mosaic:default')
            self.applyProfile(portal, 'ps.plone.mlstiles:support_mosaic')

        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

        # Prevent kss validation errors in Plone 4.2
        portal_kss = getattr(portal, 'portal_kss', None)
        if portal_kss:
            kss = portal_kss.getResource('++resource++plone.app.z3cform')
            kss.setEnabled(False)


PS_PLONE_MLSTILES_FIXTURE = PSPloneMLSTiles()
PS_PLONE_MLSTILES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PS_PLONE_MLSTILES_FIXTURE, ),
    name='PSPloneMLSTiles:Integration',
)
