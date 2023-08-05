# -*- coding: utf-8 -*-
"""Test Listing Collection tiles."""

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

# local imports
from ps.plone.mlstiles.testing import (
    PS_PLONE_MLSTILES_INTEGRATION_TESTING,
    skip_if_no_cover,
)


class ListingCollectionTileTestCase(TestTileMixin, unittest.TestCase):
    """Validate the listing collection tile."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    @skip_if_no_cover
    def setUp(self):
        from ps.plone.mlstiles.support.cover import listing_collection
        super(ListingCollectionTileTestCase, self).setUp()
        self.tile = listing_collection.ListingCollectionTile(
            self.cover,
            self.request,
        )
        self.tile.__name__ = u'ps.plone.mlstiles.listings.collection'
        self.tile.id = u'test'

    @skip_if_no_cover
    def test_interface(self):
        """Validate the tile implementation."""
        from ps.plone.mlstiles.support.cover import listing_collection
        self.interface = listing_collection.IListingCollectionTile
        self.klass = listing_collection.ListingCollectionTile
        super(ListingCollectionTileTestCase, self).test_interface()

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
    def test_delete_collection(self):
        """Validate behavior when the collection is removed."""
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)
        rendered = self.tile()

        self.assertIn(
            "<p>The collection doesn't have any results.</p>",
            rendered,
        )

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['mandelbrot-set'])

        msg = 'Please drop a collection here to fill the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())


class RecentListingsTileTestCase(TestTileMixin, unittest.TestCase):
    """Validate the recent listings tile."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    @skip_if_no_cover
    def setUp(self):
        from ps.plone.mlstiles.support.cover import listing_collection
        super(RecentListingsTileTestCase, self).setUp()
        self.tile = listing_collection.RecentListingsTile(
            self.cover,
            self.request,
        )
        self.tile.__name__ = u'ps.plone.mlstiles.listings.recent'
        self.tile.id = u'test'

    @skip_if_no_cover
    def test_interface(self):
        """Validate the tile implementation."""
        from ps.plone.mlstiles.support.cover import listing_collection
        self.interface = listing_collection.IListingCollectionTile
        self.klass = listing_collection.RecentListingsTile
        super(RecentListingsTileTestCase, self).test_interface()

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
    def test_delete_collection(self):
        """Validate behavior when the collection is removed."""
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)
        rendered = self.tile()

        self.assertIn(
            "<p>The collection doesn't have any results.</p>",
            rendered,
        )

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['mandelbrot-set'])

        msg = 'Please drop a collection here to fill the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())


class FeaturedListingsTileTestCase(TestTileMixin, unittest.TestCase):
    """Validate the featured listings tile."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    @skip_if_no_cover
    def setUp(self):
        super(FeaturedListingsTileTestCase, self).setUp()
        from ps.plone.mlstiles.support.cover import listing_collection
        self.tile = listing_collection.FeaturedListingsTile(
            self.cover,
            self.request,
        )
        self.tile.__name__ = u'ps.plone.mlstiles.listings.featured'
        self.tile.id = u'test'

    @skip_if_no_cover
    def test_interface(self):
        """Validate the tile implementation."""
        from ps.plone.mlstiles.support.cover import listing_collection
        self.interface = listing_collection.IListingCollectionTile
        self.klass = listing_collection.FeaturedListingsTile
        super(FeaturedListingsTileTestCase, self).test_interface()

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
    def test_delete_collection(self):
        """Validate behavior when the collection is removed."""
        obj = self.portal['mandelbrot-set']
        self.tile.populate_with_object(obj)
        rendered = self.tile()

        self.assertIn(
            "<p>The collection doesn't have any results.</p>",
            rendered,
        )

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)
        api.content.delete(obj=self.portal['mandelbrot-set'])

        msg = 'Please drop a collection here to fill the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())
