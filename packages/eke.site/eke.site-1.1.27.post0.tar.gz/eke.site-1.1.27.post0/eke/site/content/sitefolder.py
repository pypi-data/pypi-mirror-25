# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Site folder.'''

from eke.site import ProjectMessageFactory as _
from eke.site.config import PROJECTNAME
from eke.site.interfaces import ISiteFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from eke.knowledge.content import knowledgefolder

SiteFolderSchema = knowledgefolder.KnowledgeFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'peopleDataSource',
        required=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'People RDF Data Source'),
            description=_(u'URL to a source of registered person data in Resource Description Format.'),
            size=60,
        ),
    ),
))

finalizeATCTSchema(SiteFolderSchema, folderish=True, moveDiscussion=False)

class SiteFolder(knowledgefolder.KnowledgeFolder):
    '''Site folder which contains sites.'''
    implements(ISiteFolder)
    portal_type               = 'Site Folder'
    _at_rename_after_creation = True
    schema                    = SiteFolderSchema
    peopleDataSource          = atapi.ATFieldProperty('peopleDataSource')

atapi.registerType(SiteFolder, PROJECTNAME)
