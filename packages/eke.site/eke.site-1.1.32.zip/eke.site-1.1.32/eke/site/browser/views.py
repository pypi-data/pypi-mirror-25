# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Sites: views for content types.
'''

from Acquisition import aq_inner
from eke.knowledge.browser.views import KnowledgeFolderView, KnowledgeObjectView
from eke.site.interfaces import ISite, ISiteFolder, IPerson
from eke.publications.interfaces import IPublication
from eke.study.interfaces import IProtocol
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
import logging, plone.api

_logger = logging.getLogger('Plone')

_edrnSiteTypes = frozenset((
    u'Biomarker Reference Laboratories',
    u'Biomarker Developmental Laboratories',
    u'Clinical Validation Centers',
    u'Data Management and Coordinating Center',
    u'Informatics Center',
    u'National Cancer Institute',
    u'Associate Member A - EDRN Funded',
    u'Associate Member B',
    u'Associate Member C',
    u'SPOREs',
))


class SiteFolderView(KnowledgeFolderView):
    '''Default view of a Site folder.'''
    __call__ = ViewPageTemplateFile('templates/sitefolder.pt')
    def _sortByInvestigator(self, sitesList):
        sitesList.sort(lambda a, b: cmp(a['investigator'], b['investigator']))
    def _sortBySiteName(self, sitesList):
        sitesList.sort(lambda a, b: cmp(a['title'], b['title']))
    def _transformTypeName(self, memberType):
        if memberType.startswith(u'Associate Member C') or memberType.startswith(u'Assocaite Member C'):  # Thanks, DMCC
            return u'Associate Member C'
        elif memberType.startswith(u'Associate Member B'):
            return u'Associate Member B'
        elif memberType == u'Clinical Validation Center':
            return u'Clinical Validation Centers'  # CA-680
        elif memberType == u'SPORE':
            return u'SPOREs'  # CA-697
        else:
            return unicode(memberType)
    @memoize
    def biomarkerDevelopmentalLaboratories(self):
        context = aq_inner(self.context)
        catalog, uidCatalog = getToolByName(context, 'portal_catalog'), getToolByName(context, 'uid_catalog')
        results = catalog(
            object_provides=ISite.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            memberType=(u'Biomarker Developmental Laboratories', u'Biomarker Developmental  Laboratories')  # Thanks, DMCC
        )
        byOrgan = {}
        for brain in results:
            organNames = len(brain.organs) == 0 and ('',) or brain.organs
            for organName in organNames:
                if organName not in byOrgan: byOrgan[organName] = {}
                proposals = byOrgan[organName]
                if brain.proposal not in proposals: proposals[brain.proposal] = []
                sites = proposals[brain.proposal]
                if brain.piUID:
                    uidBrain = uidCatalog(UID=brain.piUID)[0]
                    piURL = uidBrain.getURL(relative=False)
                    piName = uidBrain.Title
                else:
                    piURL = piName = None
                sites.append(dict(
                    title=brain.Title,
                    description=brain.Description,
                    investigator=piName,
                    piURL=piURL,
                    url=brain.getURL(),
                    specialty=brain.specialty
                ))
        organs = []
        for organName, proposals in byOrgan.items():
            propGroup = []
            for proposalName, sites in proposals.items():
                propGroup.append(dict(title=proposalName, sites=sites))
            propGroup.sort(lambda a, b: (not a['title'] and not b['title']) and 1 or cmp(a['title'], b['title']))
            organs.append(dict(title=organName, proposalGroups=propGroup))
        organs.sort(lambda a, b: (not a['title'] and not b['title']) and 1 or cmp(a['title'], b['title']))
        return organs
    @memoize
    def biomarkerReferenceLaboratories(self):
        allSites = self._sites()
        try:
            brls = allSites[u'Biomarker Reference Laboratories']
            self._sortByInvestigator(brls)
            return brls
        except KeyError:
            return []
    @memoize
    def clinicalValidationCenters(self):
        allSites = self._sites()
        try:
            cvcs = allSites[u'Clinical Validation Centers']
            self._sortByInvestigator(cvcs)
            return cvcs
        except KeyError:
            return []
    @memoize
    def dmccSites(self):
        allSites = self._sites()
        try:
            dmccs = allSites[u'Data Management and Coordinating Center']
            self._sortBySiteName(dmccs)
            return dmccs
        except KeyError:
            return []
    @memoize
    def icSites(self):
        allSites = self._sites()
        try:
            ics = allSites[u'Informatics Center']
            self._sortBySiteName(ics)
            return ics
        except KeyError:
            return []
    def nciSites(self):
        allSites = self._sites()
        try:
            ncis = allSites[u'National Cancer Institute']
            self._sortByInvestigator(ncis)
            return ncis
        except KeyError:
            return []
    def typeASites(self):
        allSites = self._sites()
        try:
            sites = allSites[u'Associate Member A - EDRN Funded']
            self._sortBySiteName(sites)
            return sites
        except KeyError:
            return []
    def typeBSites(self):
        allSites = self._sites()
        try:
            sites = allSites[u'Associate Member B']
            self._sortBySiteName(sites)
            return sites
        except KeyError:
            return []
    def typeCSites(self):
        allSites = self._sites()
        try:
            sites = allSites[u'Associate Member C']
            self._sortBySiteName(sites)
            return sites
        except KeyError:
            return []
    def sporeSites(self):
        allSites = self._sites()
        try:
            sites = allSites[u'SPOREs']
            self._sortBySiteName(sites)
            return sites
        except KeyError:
            return []
    def otherSites(self):
        allSites, otherSites = self._sites(), {}
        for memberType, sites in allSites.items():
            if memberType not in _edrnSiteTypes:
                otherSites[memberType] = sites
                self._sortBySiteName(sites)
        otherSites = [dict(memberType=memberType, sites=sites) for memberType, sites in otherSites.items()]
        otherSites.sort(lambda a, b: cmp(a['memberType'], b['memberType']))
        return otherSites
    @memoize
    def _sites(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        uidCatalog = getToolByName(context, 'uid_catalog')
        results = catalog(
            object_provides=ISite.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='memberType'
        )
        sites = {}
        for i in results:
            memberType = self._transformTypeName(i.memberType.strip())
            if not memberType:
                # CA-609: skip 'em
                continue
            if memberType not in sites:
                sites[memberType] = []
            if i.piUID:
                uidBrain = uidCatalog(UID=i.piUID)[0]
                piURL = uidBrain.getURL(relative=False)
                piName = uidBrain.Title
            else:
                piURL = piName = None
            sites[memberType].append(dict(
                title=i.Title,
                description=i.Description,
                investigator=piName,
                piURL=piURL,
                organs=i.organs,
                proposal=i.proposal,
                url=i.getURL(),
                specialty=i.specialty
            ))
        return sites
    @memoize
    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=ISiteFolder.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]


class SiteView(KnowledgeObjectView):
    '''Default view of a site.'''
    __call__ = ViewPageTemplateFile('templates/site.pt')
    def haveStaff(self):
        staff = self.staff()
        return len(staff) > 0
    @memoize
    def staff(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IPerson.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
        )
        staff = dict([(i.UID, dict(name=i.Title, url=i.getURL())) for i in results])
        anointed = set()
        if context.getRawPrincipalInvestigator() is not None:
            anointed.add(context.getRawPrincipalInvestigator())
        for investigators in (
            context.getRawCoPrincipalInvestigators(), context.getRawCoInvestigators(), context.getRawInvestigators()
        ):
            anointed |= set(investigators)
        for investigator in anointed:
            if investigator in staff:
                del staff[investigator]
        staff = staff.values()
        staff.sort()
        return staff
    def showSponsor(self):
        '''Tell if the sponsor for this site should be displayed (CA-666)'''
        context = aq_inner(self.context)
        memberType = context.memberType
        if not memberType:
            return False
        memberType = memberType.strip()
        return memberType.startswith('Associate') or memberType.startswith('Assocaite')  # Thanks, DMCC. Ugh. >_<
    def showOrgans(self):
        '''Should we show our organs of interest?'''
        context = aq_inner(self.context)
        return context.memberType in (
            u'Biomarker Developmental Laboratories',
            u'Biomarker Developmental  Laboratories',  # Thanks, DMCC.
            u'Clinical Validation Center',
            u'Clinical Validation Centers',  # CA-680
        )


class PersonView(KnowledgeObjectView):
    '''Default view of a Person.'''
    __call__ = ViewPageTemplateFile('templates/person.pt')
    @memoize
    def bespokeURL(self):
        context = aq_inner(self.context)
        portal = plone.api.portal.get()
        if 'member-pages' not in portal.keys(): return None
        memberPages = portal['member-pages']
        if context.accountName not in memberPages.keys(): return None
        memberPage = memberPages[context.accountName]
        state = plone.api.content.get_state(obj=memberPage)
        if state == 'private': return None
        return memberPage.absolute_url()
    @memoize
    def protocols(self):
        context = aq_inner(self.context)
        catalog = plone.api.portal.get_tool('portal_catalog')
        leadpi_results = catalog(
            object_provides=IProtocol.__identifier__,
            sort_on='sortable_title',
            piUID=context.piUID
        )
        involved_results = catalog(
            object_provides=IProtocol.__identifier__,
            sort_on='sortable_title',
            involvedInvestigatorUID=context.piUID
        )
        actives, inactives = [], []
        all_results = leadpi_results + involved_results
        existingProtocols = {}
        for i in all_results:
            protocol = i.getObject()
            if protocol.absolute_url() in existingProtocols:
                continue
            else:
                existingProtocols[protocol.absolute_url()] = 1
            if protocol.involvedInvestigatorUID:
                if context.piUID in protocol.involvedInvestigatorUID:
                    if protocol.finishDate:
                        inactives.append(protocol)
                    else:
                        actives.append(protocol)
        return actives, inactives
    @memoize
    def publications(self):
        context = aq_inner(self.context)
        catalog = plone.api.portal.get_tool('portal_catalog')
        results = catalog(
            object_provides=IPublication.__identifier__,
            siteID=context.siteID
        )
        publications = []
        for i in results:
            publications.append(i.getObject())
        return publications
