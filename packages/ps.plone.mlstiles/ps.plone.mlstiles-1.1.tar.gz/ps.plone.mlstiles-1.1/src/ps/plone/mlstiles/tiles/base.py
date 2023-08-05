# -*- coding: utf-8 -*-
"""Base and helper classes for tiles."""

# zope imports
try:
    from plone.app.vocabularies.catalog import (
        CatalogSource as CatalogSourceBase,
    )
    HAS_CATALOG_SOURCE = True
except ImportError:
    from plone.app.vocabularies.catalog import (
        SearchableTextSourceBinder as CatalogSourceBase,
    )
    HAS_CATALOG_SOURCE = False


class CatalogSource(CatalogSourceBase):
    """Specific catalog source to allow targeted widget."""

    def __init__(self, context=None, **query):
        if HAS_CATALOG_SOURCE:
            return super(CatalogSource, self).__init__(
                context=context, **query
            )
        else:
            return super(CatalogSource, self).__init__(query)

    def __contains__(self, value):
        """Return always contains to allow lazy handling of removed objs."""
        return True
