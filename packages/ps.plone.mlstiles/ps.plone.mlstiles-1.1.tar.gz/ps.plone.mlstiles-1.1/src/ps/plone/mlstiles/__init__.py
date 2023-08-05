# -*- coding: utf-8 -*-
"""Tiles support for the Propertyshelf MLS Plone Embedding."""

# zope imports
from plone import api as ploneapi
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('ps.plone.mlstiles')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


PLONE_4 = '4' <= ploneapi.env.plone_version() < '5'
PLONE_5 = '5' <= ploneapi.env.plone_version() < '6'
