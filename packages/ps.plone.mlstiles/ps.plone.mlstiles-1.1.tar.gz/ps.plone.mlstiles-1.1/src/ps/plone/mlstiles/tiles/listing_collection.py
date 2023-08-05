# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS listings."""

# python imports
import copy

# zope imports
from plone import api as plone_api
from plone.memoize import view
from plone.mls.listing import api
from plone.mls.listing.browser.listing_collection import (
    CONFIGURATION_KEY as LC_CONFIGURATION_KEY,
    IListingCollection,
)
from plone.mls.listing.browser.listing_search import (
    CONFIGURATION_KEY as SEARCH_CONFIGURATION_KEY,
    IListingSearch,
)
from plone.mls.listing.browser.recent_listings import (
    CONFIGURATION_KEY as RL_CONFIGURATION_KEY,
    IRecentListings,
)
from ps.plone.mls.browser.listings import featured
from zope.annotation.interfaces import IAnnotations


class ListingCollectionTileMixin(object):
    """A tile that shows a list of MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(LC_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IListingCollection.providedBy(obj)

    @property
    def get_context(self):
        """Return the listing collection context."""
        raise NotImplementedError

    @property
    def size(self):
        raise NotImplementedError

    @property
    def start_at(self):
        raise NotImplementedError

    @property
    @view.memoize
    def items(self):
        """Return the collection items."""
        items = []
        context = self.get_context
        if not context or not self.has_listing_collection(context):
            return items

        context_config = copy.copy(self.get_config(context))
        language = plone_api.portal.get_current_language(context=context)
        params = {
            'lang': language,
            'limit': self.size,
            'offset': self.start_at,
        }
        context_config.update(params)
        params = api.prepare_search_params(context_config)
        items = api.search(
            params=params,
            batching=False,
            context=context,
            config=self.get_config(context),
        )
        return items


class ListingSearchResultsTileMixin(ListingCollectionTileMixin):
    """A tile that shows a list of MLS listings from search results."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(SEARCH_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for listing search results."""
        return IListingSearch.providedBy(obj)


class RecentListingsTileMixin(ListingCollectionTileMixin):
    """A tile that shows a list of recent MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(RL_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IRecentListings.providedBy(obj)


class FeaturedListingsTileMixin(ListingCollectionTileMixin):
    """A tile that shows a list of featured MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(featured.CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return featured.IFeaturedListings.providedBy(obj)
