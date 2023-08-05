# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments for plone.app.mosaic."""

# zope imports
from plone import api
from plone.app.standardtiles import _PMF
from plone.memoize import view
from plone.supermodel.model import Schema
from plone.tiles import Tile
from ps.plone.mls.interfaces import IDevelopmentCollection
from zope import schema

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.base import CatalogSource
from ps.plone.mlstiles.tiles.development_collection import (
    DevelopmentCollectionTileMixin,
)


class IDevelopmentCollectionTile(Schema):
    """Configuration schema for a development collection."""

    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IDevelopmentCollection.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing development collection'),
    )

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
        title=_(u'Show development title'),
    )

    title_level = schema.Choice(
        default=u'h3',
        required=False,
        title=_(u'Development title level'),
        values=(u'h1', u'h2', u'h3', u'h4', u'h5', u'h6'),
    )

    show_description = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development description'),
    )

    show_banner = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development banner image'),
    )

    show_logo = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development logo'),
    )

    show_location = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location information for a development'),
    )

    show_lot_size = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show lot size information for a development'),
    )

    show_location_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location type information for a development'),
    )

    show_number_of_listings = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show number of listings for a development'),
    )

    show_number_of_groups = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show number of groups for a development'),
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


class DevelopmentCollectionTile(DevelopmentCollectionTileMixin, Tile):
    """A tile that shows a list of MLS developments."""

    @property
    def tile_class(self):
        css_class = 'development__results'
        additional_classes = self.data.get('tile_class', '')
        if not additional_classes:
            return css_class
        return ' '.join([css_class, additional_classes])

    @property
    @view.memoize
    def get_context(self):
        """Return the development collection context."""
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

    def get_fields(self):
        fields = super(DevelopmentCollectionTile, self).get_fields()
        if self.data.get('show_banner'):
            fields.append('banner_image')
        return fields
