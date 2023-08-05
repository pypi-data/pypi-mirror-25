# -*- coding: utf-8 -*-
"""Test Listing Search tile."""

# python imports
from mock import Mock
import unittest

# zope imports
try:
    from collective.cover.testing import ALL_CONTENT_TYPES
    from collective.cover.tests.base import TestTileMixin
except ImportError:
    ALL_CONTENT_TYPES = []

    class TestTileMixin(object):
        """Dummy class"""
from plone import api
from plone.app.testing import (
    TEST_USER_ID,
    TEST_USER_NAME,
    login,
    setRoles,
)

from ps.plone.mlstiles.testing import (
    PS_PLONE_MLSTILES_INTEGRATION_TESTING,
    skip_if_no_cover,
)


class ListingSearchTileTestCase(TestTileMixin, unittest.TestCase):
    """Validate the listing search tile."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    @skip_if_no_cover
    def setUp(self):
        from ps.plone.mlstiles.support.cover import listing_search
        super(ListingSearchTileTestCase, self).setUp()
        self.tile = listing_search.ListingSearchTile(self.cover, self.request)
        self.tile.__name__ = u'ps.plone.mlstiles.listings.search'
        self.tile.id = u'test'

    @skip_if_no_cover
    def test_interface(self):
        """Validate the tile implementation."""
        from ps.plone.mlstiles.support.cover import listing_search
        self.interface = listing_search.IListingSearchTile
        self.klass = listing_search.ListingSearchTile
        super(ListingSearchTileTestCase, self).test_interface()

    @skip_if_no_cover
    def test_default_configuration(self):
        """Validate the default tile configuration."""
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    @skip_if_no_cover
    def test_accepted_content_types(self):
        """Validate the accepted content types for the tile."""
        self.assertEqual(self.tile.accepted_ct(), ALL_CONTENT_TYPES)

    @skip_if_no_cover
    def test_tile_is_empty(self):
        """Validate that the tile is empty by default."""
        self.assertTrue(self.tile.is_empty())

    @skip_if_no_cover
    def test_delete_content(self):
        """Validate behavior when the content is removed."""
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)
        rendered = self.tile()
        self.assertNotIn('form', rendered)

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['mandelbrot-set'])

        msg = 'Please drag&amp;drop some content here to populate the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())
