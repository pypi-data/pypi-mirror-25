# -*- coding: utf-8 -*-
"""MLS listing search tile."""

# zope imports
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _ as _CC
from collective.cover.tiles import base
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api as ploneapi
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
from plone.mls.listing.i18n import _ as _MLS
from plone.tiles.interfaces import (
    ITileDataManager,
    ITileType,
)
from zope import schema
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema import getFieldNamesInOrder
from zope.schema.fieldproperty import FieldProperty

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.listing_search import ListingSearchTileMixin


class IListingSearchTile(base.IPersistentCoverTile):
    """Configuration schema for a listing search."""

    header = schema.TextLine(
        required=False,
        title=_CC(u'Header'),
    )

    form.omitted('form_q')
    form.no_omit(IDefaultConfigureForm, 'form_q')
    form_q = schema.Text(
        required=False,
        title=_MLS(u'Freetext search (Location, Keywords, Listing ID, ...)'),
    )

    form.omitted('form_listing_type')
    form.no_omit(IDefaultConfigureForm, 'form_listing_type')
    form_listing_type = schema.Text(
        required=False,
        title=_MLS(u'Listing Type'),
    )

    form.omitted('form_location_state')
    form.no_omit(IDefaultConfigureForm, 'form_location_state')
    form_location_state = schema.Text(
        required=False,
        title=_MLS(u'State'),
    )

    form.omitted('form_location_county')
    form.no_omit(IDefaultConfigureForm, 'form_location_county')
    form_location_county = schema.Text(
        required=False,
        title=_MLS(u'County'),
    )

    form.omitted('form_location_district')
    form.no_omit(IDefaultConfigureForm, 'form_location_district')
    form_location_district = schema.Text(
        required=False,
        title=_MLS(u'District'),
    )

    form.omitted('form_location_city')
    form.no_omit(IDefaultConfigureForm, 'form_location_city')
    form_location_city = schema.Text(
        required=False,
        title=_MLS(u'City/Town'),
    )

    form.omitted('form_price_min')
    form.no_omit(IDefaultConfigureForm, 'form_price_min')
    form_price_min = schema.Text(
        required=False,
        title=_MLS(u'Price (Min)'),
    )

    form.omitted('form_price_max')
    form.no_omit(IDefaultConfigureForm, 'form_price_max')
    form_price_max = schema.Text(
        required=False,
        title=_MLS(u'Price (Max)'),
    )

    form.omitted('form_location_type')
    form.no_omit(IDefaultConfigureForm, 'form_location_type')
    form_location_type = schema.Text(
        required=False,
        title=_MLS(u'Location Type'),
    )

    form.omitted('form_geographic_type')
    form.no_omit(IDefaultConfigureForm, 'form_geographic_type')
    form_geographic_type = schema.Text(
        required=False,
        title=_MLS(u'Geographic Type'),
    )

    form.omitted('form_view_type')
    form.no_omit(IDefaultConfigureForm, 'form_view_type')
    form_view_type = schema.Text(
        required=False,
        title=_MLS(u'View Type'),
    )

    form.omitted('form_object_type')
    form.no_omit(IDefaultConfigureForm, 'form_object_type')
    form_object_type = schema.Text(
        required=False,
        title=_MLS(u'Object Type'),
    )

    form.omitted('form_ownership_type')
    form.no_omit(IDefaultConfigureForm, 'form_ownership_type')
    form_ownership_type = schema.Text(
        required=False,
        title=_MLS(u'Ownership Type'),
    )

    form.omitted('form_beds')
    form.no_omit(IDefaultConfigureForm, 'form_beds')
    form_beds = schema.Text(
        required=False,
        title=_MLS(u'Bedrooms'),
    )

    form.omitted('form_baths')
    form.no_omit(IDefaultConfigureForm, 'form_baths')
    form_baths = schema.Text(
        required=False,
        title=_MLS(u'Bathrooms'),
    )

    form.omitted('form_air_condition')
    form.no_omit(IDefaultConfigureForm, 'form_air_condition')
    form_air_condition = schema.Text(
        required=False,
        title=_MLS(u'Air Condition'),
    )

    form.omitted('form_pool')
    form.no_omit(IDefaultConfigureForm, 'form_pool')
    form_pool = schema.Text(
        required=False,
        title=_MLS(u'Pool'),
    )

    form.omitted('form_jacuzzi')
    form.no_omit(IDefaultConfigureForm, 'form_jacuzzi')
    form_jacuzzi = schema.Text(
        required=False,
        title=_MLS(u'Jacuzzi'),
    )

    form.omitted('form_lot_size')
    form.no_omit(IDefaultConfigureForm, 'form_lot_size')
    form_lot_size = schema.Text(
        required=False,
        title=_MLS(u'Lot Size'),
    )

    form.omitted('form_interior_area')
    form.no_omit(IDefaultConfigureForm, 'form_interior_area')
    form_interior_area = schema.Text(
        required=False,
        title=_MLS(u'Interior Area'),
    )

    footer = schema.TextLine(
        required=False,
        title=_CC(u'Footer'),
    )

    uuid = schema.TextLine(
        readonly=True,
        title=_CC(u'UUID'),
    )


@implementer(IListingSearchTile)
class ListingSearchTile(ListingSearchTileMixin, base.PersistentCoverTile):
    """A tile that shows a search form for listings."""

    is_configurable = True
    is_editable = True
    short_name = _(u'MLS: Listing Search')
    index = ViewPageTemplateFile('listing_search.pt')

    header = FieldProperty(IListingSearchTile['header'])

    form_q = FieldProperty(IListingSearchTile['form_q'])
    form_listing_type = FieldProperty(IListingSearchTile['form_listing_type'])
    form_location_state = FieldProperty(
        IListingSearchTile['form_location_state']
    )
    form_location_county = FieldProperty(
        IListingSearchTile['form_location_county']
    )
    form_location_district = FieldProperty(
        IListingSearchTile['form_location_district']
    )
    form_location_city = FieldProperty(
        IListingSearchTile['form_location_city']
    )
    form_price_min = FieldProperty(IListingSearchTile['form_price_min'])
    form_price_max = FieldProperty(IListingSearchTile['form_price_max'])
    form_location_type = FieldProperty(
        IListingSearchTile['form_location_type']
    )
    form_geographic_type = FieldProperty(
        IListingSearchTile['form_geographic_type']
    )
    form_view_type = FieldProperty(IListingSearchTile['form_view_type'])
    form_object_type = FieldProperty(IListingSearchTile['form_object_type'])
    form_ownership_type = FieldProperty(
        IListingSearchTile['form_ownership_type']
    )
    form_beds = FieldProperty(IListingSearchTile['form_beds'])
    form_baths = FieldProperty(IListingSearchTile['form_baths'])
    form_air_condition = FieldProperty(
        IListingSearchTile['form_air_condition']
    )
    form_pool = FieldProperty(IListingSearchTile['form_pool'])
    form_jacuzzi = FieldProperty(IListingSearchTile['form_jacuzzi'])
    form_lot_size = FieldProperty(IListingSearchTile['form_lot_size'])
    form_interior_area = FieldProperty(
        IListingSearchTile['form_interior_area']
    )

    footer = FieldProperty(IListingSearchTile['footer'])
    uuid = FieldProperty(IListingSearchTile['uuid'])

    def get_title(self):
        return self.data['title']

    def is_empty(self):
        return self.data.get('uuid', None) is None or \
            uuidToObject(self.data.get('uuid')) is None

    def populate_with_object(self, obj):
        # Check permission.
        super(ListingSearchTile, self).populate_with_object(obj)

        if obj.portal_type in self.accepted_ct():
            # Use obj's title as header.
            header = safe_unicode(obj.Title())
            footer = _CC(u'More…')
            uuid = ploneapi.content.get_uuid(obj)

            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'header': header,
                'footer': footer,
                'uuid': uuid,
            })

    def remove_relation(self):
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if 'uuid' in old_data:
            old_data.pop('uuid')
        data_mgr.set(old_data)

    def show_header(self):
        return self._field_is_visible('header')

    @property
    def available_fields(self):
        fields = []
        tile_type = queryUtility(ITileType, name=self.__name__)
        conf = self.get_tile_configuration()
        for name in getFieldNamesInOrder(tile_type.schema):
            if name in conf:
                field_conf = conf[name]
                if ('visibility' in field_conf and
                        field_conf['visibility'] == u'off'):
                    # If the field was configured to be invisible, then just
                    # ignore it
                    continue
            if name.startswith('form_'):
                fields.append(name.split('form_')[1])
        return fields

    def show_footer(self):
        return self._field_is_visible('footer')

    @property
    def get_context(self):
        """Return the development collection context."""
        uuid = self.data.get('uuid', None)
        if uuid is None:
            return
        item = ploneapi.content.get(UID=uuid)
        return item
