# encoding: utf-8
# Copyright 2010–2017 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from . import DEFAULT_PROFILE_ID
from Products.CMFCore.utils import getToolByName
from eke.study.interfaces import IProtocol


def addProtocolIDs(setupTool):
    '''Prepend the protocol ID to each protocol's object ID.'''
    portal = getToolByName(setupTool, 'portal_url').getPortalObject()
    catalog = getToolByName(portal, 'portal_catalog')
    results = catalog(object_provides=IProtocol.__identifier__)
    for i in results:
        o = i.getObject()
        newID = str(o.identifier.split('/')[-1]) + '-' + o.getId()
        o.setId(newID)


def nullUpgradeStep(setupTool):
    pass


def updateCatalog(setupTool):
    setupTool.runImportStepFromProfile(DEFAULT_PROFILE_ID, 'catalog')
