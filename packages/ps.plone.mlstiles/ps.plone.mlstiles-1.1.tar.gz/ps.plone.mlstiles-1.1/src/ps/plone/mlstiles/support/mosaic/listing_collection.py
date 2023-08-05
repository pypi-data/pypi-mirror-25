# -*- coding: utf-8 -*-
"""Tiles that shows a list of MLS listings for plone.app.mosaic."""

# zope imports
from plone import api
from plone.app.standardtiles import _PMF
from plone.autoform import directives
from plone.mls.listing.browser.listing_collection import IListingCollection
from plone.mls.listing.browser.listing_search import IListingSearch
from plone.mls.listing.browser.recent_listings import IRecentListings
from plone.memoize import view
from plone.supermodel.model import Schema
from plone.tiles import Tile
from ps.plone.mls.browser.listings.featured import IFeaturedListings
from zope import schema

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.base import CatalogSource
from ps.plone.mlstiles.tiles.listing_collection import (
    FeaturedListingsTileMixin,
    ListingCollectionTileMixin,
    ListingSearchResultsTileMixin,
    RecentListingsTileMixin,
)


class IBaseCollectionTile(Schema):
    """Base configuration schema for listing collections."""

    count = schema.Int(
        default=5,
        required=False,
        title=_(u'Number of items to display'),
    )

    offset = schema.Int(
        default=0,
        required=False,
        title=_(u'Start at item'),
    )

    tile_title = schema.TextLine(
        required=False,
        title=_(u'Tile Headline'),
    )

    show_tile_title = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show tile headline'),
    )

    tile_title_level = schema.Choice(
        default=u'h2',
        required=False,
        title=_(u'Tile headline level'),
        values=(u'h1', u'h2', u'h3', u'h4', u'h5', u'h6'),
    )

    show_title = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show listing title'),
    )

    title_level = schema.Choice(
        default=u'h3',
        required=False,
        title=_(u'Listing title level'),
        values=(u'h1', u'h2', u'h3', u'h4', u'h5', u'h6'),
    )

    show_description = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show listing description'),
    )

    show_image = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show listing image'),
    )

    show_price = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show price information for a listing'),
    )

    show_workflow_status = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show workflow status for a listing'),
    )

    show_listing_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show listing type'),
    )

    show_number_of_images = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show number of images for a listing'),
    )

    show_object_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show property type information for a listing'),
    )

    show_beds_baths = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show bedroom and bathroom information for a listing'),
    )

    show_location = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location information for a listing'),
    )

    show_location_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location type information for a listing'),
    )

    show_view_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show view type information for a listing'),
    )

    show_lot_size = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show lot size information for a listing'),
    )

    show_living_area = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show living area information for a listing'),
    )

    show_interior_area = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show interior area information for a listing'),
    )

    show_more_link = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show link to collection'),
    )

    more_link_text = schema.TextLine(
        default=_(u'More...'),
        required=False,
        title=_(u'Text for link to collection'),
    )

    tile_class = schema.TextLine(
        default=u'',
        description=_PMF(
            u'Insert a list of additional CSS classes that will ',
            u'be added to the tile',
        ),
        required=False,
        title=_PMF(u'Tile additional styles'),
    )


class IListingCollectionTile(IBaseCollectionTile):
    """Configuration schema for a listing collection."""

    directives.order_before(content_uid='*')
    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IListingCollection.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing listing collection'),
    )


class IListingSearchResultsTile(IBaseCollectionTile):
    """Configuration schema for a listing search (results)."""

    directives.order_before(content_uid='*')
    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IListingSearch.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing listing search'),
    )


class IRecentListingsTile(IBaseCollectionTile):
    """Configuration schema for a recent listings collection."""

    directives.order_before(content_uid='*')
    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IRecentListings.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing recent listing collection'),
    )


class IFeaturedListingsTile(IBaseCollectionTile):
    """Configuration schema for a featured listings collection."""

    directives.order_before(content_uid='*')
    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IFeaturedListings.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing featured listings collection'),
    )


class ListingCollectionTile(ListingCollectionTileMixin, Tile):
    """A tile that shows a list of MLS listings."""

    @property
    def tile_class(self):
        css_class = 'listing__results'
        additional_classes = self.data.get('tile_class', '')
        if not additional_classes:
            return css_class
        return ' '.join([css_class, additional_classes])

    @property
    @view.memoize
    def get_context(self):
        """Return the listing collection context."""
        uuid = self.data.get('content_uid')
        if uuid != api.content.get_uuid(obj=self.context):
            item = api.content.get(UID=uuid)
            if item is not None:
                return item
        return None

    @property
    def size(self):
        return self.data.get('count')

    @property
    def start_at(self):
        return self.data.get('offset')


class ListingSearchResultsTile(
    ListingSearchResultsTileMixin,
    ListingCollectionTile,
):
    """A tile that shows a list of MLS listings from search results."""


class RecentListingsTile(RecentListingsTileMixin, ListingCollectionTile):
    """A tile that shows a list of recent MLS listings."""


class FeaturedListingsTile(FeaturedListingsTileMixin, ListingCollectionTile):
    """A tile that shows a list of featured MLS listings."""
