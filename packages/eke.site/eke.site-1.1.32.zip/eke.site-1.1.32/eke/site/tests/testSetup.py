# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Sites: test the setup of this package.
'''

import unittest2 as unittest
from eke.site.testing import EKE_SITE_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.app.testing import TEST_USER_ID, setRoles, login, TEST_USER_NAME

class SetupTest(unittest.TestCase):
    '''Unit tests the setup of this package.'''
    layer = EKE_SITE_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testCatalogIndexes(self):
        '''Check if indexes are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for i in ('memberType', 'siteID', 'piUID', 'investigatorStatus', 'organs', 'proposal', 'accountName'):
            self.failUnless(i in indexes, i + ' index is missing')
    def testCatalogMetadata(self):
        '''Check if indexed metadata schema are properly installed.'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = catalog.schema()
        for i in ('memberType', 'siteID', 'piUID', 'investigatorStatus', 'organs', 'proposal'):
            self.failUnless(i in metadata)
    def testTypes(self):
        '''Make sure our types are available.'''
        types = getToolByName(self.portal, 'portal_types')
        for i in ('Site Folder', 'Site', 'Person'):
            self.failUnless(i in types.objectIds())
            self.failIf(types[i].allow_discussion, 'Type "%s" allows discussion but should not' % i)
    def testFacetedNavigation(self):
        '''Ensure we can use facets on site folders'''
        from eke.site.content.sitefolder import SiteFolder
        from eea.facetednavigation.interfaces import IPossibleFacetedNavigable
        self.failUnless(IPossibleFacetedNavigable.implementedBy(SiteFolder))
    def testVocabulaies(self):
        '''Verify that our vocabularies are available'''
        vocabs = (
            u'Sites', u'People', u'PeopleWithNoReference', u'PrincipalInvestigators', u'NotPeons', u'MemberType', u'SitesNames',
            u'SitesWithNoReference'
        )
        for v in vocabs:
            vocabName = u'eke.site.' + v
            vocab = queryUtility(IVocabularyFactory, name=vocabName)
            self.failIf(vocab is None, u'Vocabulary "%s" not available' % vocabName)
    def testNotPeonsVocabulary(self):
        u'''Ensure that the not-peons vocabulary stores string values instead of booleans, since
        eea.facetednavigation chokes on booleans as values—what a piece of crap.'''
        vocabFactory = queryUtility(IVocabularyFactory, name=u'eke.site.NotPeons')
        self.failIf(vocabFactory is None)
        vocab = vocabFactory(self.portal)
        self.assertEquals(3, len(vocab))
        self.assertEquals(u'Staff', vocab.getTerm('staff').token)
        self.assertEquals(u'PI', vocab.getTerm('pi').token)
        self.assertEquals(u'Investigator', vocab.getTerm('investigator').token)
    def testVocabularyContextSensitivity(self):
        '''Expose CA-725: Vocabularies eke.site.People and eke.site.PeopleWithNoReference are context-dependent'''
        membershipTool = getToolByName(self.portal, 'portal_membership')
        membershipTool.addMember('manager', 'secret', ['Manager'], [])
        login(self.portal, 'manager')
        folder = self.portal[self.portal.invokeFactory('Folder', 'folder')]
        sites = self.portal[self.portal.invokeFactory('Site Folder', 'sites')]
        site = sites[sites.invokeFactory('Site', 'site')]
        site.invokeFactory('Person', 'person')
        vocabFactory = queryUtility(IVocabularyFactory, name=u'eke.site.People')
        fromFolder, fromSite = vocabFactory(folder), vocabFactory(site)
        self.assertEquals(len(fromFolder), len(fromSite))
        vocabFactory = queryUtility(IVocabularyFactory, name=u'eke.site.PeopleWithNoReference')
        fromFolder, fromSite = vocabFactory(folder), vocabFactory(site)
        self.assertEquals(len(fromFolder), len(fromSite))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
