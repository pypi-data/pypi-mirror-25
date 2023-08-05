# encoding: utf-8
# Copyright 2009-2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Sites: RDF ingest for site folders and their sites.
'''

from Acquisition import aq_inner
from eke.knowledge import dublincore
from eke.knowledge.browser.rdf import IngestHandler, KnowledgeFolderIngestor, CreatedObject, registerHandler, Results, \
    RDFIngestException
from eke.knowledge.browser.utils import MarkupFilterer
from eke.knowledge.browser.utils import updateObject, getUIDsFromURIs
from eke.site import ProjectMessageFactory as _
from eke.site.interfaces import ISite, IPerson
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from rdflib import URIRef, ConjunctiveGraph, URLInputSource
from zope.component import queryUtility
import urlparse, urllib2, mimetypes, socket, smtplib, contextlib

# CA-609: Notification when ingest of unknown sites occurs
_na      = 'edrninfo@compass.fhcrc.org' # Notification address: whom to notify
_sa      = 'kruegerk@mail.nih.gov'      # Source address: we fall back to this if no email_from_address is set in portal
_message = '''(This is an automated message from the EDRN Portal at %(portalURL)s.)

During ingest of EDRN member sites, some sites (%(numberOfSites)d, to be exact) had no member type.

These are the sites that had this problem:

%(sitesList)s''' # FIXME: not i18n

# Well-known URI refs
_coIPredicateURI          = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#coi')
_coPIPredicateURI         = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#copi')
_dcTitleURI               = URIRef(dublincore.TITLE_URI)
_givenNamePredicateURI    = URIRef('http://xmlns.com/foaf/0.1/givenname')
_investigatorPredicateURI = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#investigator')
_ma1PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailAddr1')
_ma2PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailAddr2')
_maCityPredURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailCity')
_maCountryPredURI         = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailCountry')
_maStatePredURI           = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailState')
_maZipPredURI             = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#mailZip')
_mailAddrPreds            = (_ma1PredURI, _ma2PredURI, _maCityPredURI, _maStatePredURI, _maZipPredURI, _maCountryPredURI)
_memberTypeURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#memberType')
_middleNamePredicateURI   = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#middleName')
_pa1PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physAddr1')
_pa2PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physAddr2')
_paCityPredURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physCity')
_paCountryPredURI         = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physCountry')
_paStatePredURI           = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physState')
_paZipPredURI             = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#physZip')
_physAddrPreds            = (_pa1PredURI, _pa2PredURI, _paCityPredURI, _paStatePredURI, _paZipPredURI, _paCountryPredURI)
_personTypeURI            = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Person')
_photoPredicateURI        = URIRef('http://xmlns.com/foaf/0.1/img')
_piPredicateURI           = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#pi')
_sa1PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipAddr1')
_sa2PredURI               = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipAddr2')
_saCityPredURI            = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipCity')
_saCountryPredURI         = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipCountry')
_saStatePredURI           = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipState')
_saZipPredURI             = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#shipZip')
_shipAddrPreds            = (_sa1PredURI, _sa2PredURI, _saCityPredURI, _saStatePredURI, _saZipPredURI, _saCountryPredURI)
_siteTypeURI              = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Site')
_siteURI                  = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#site')
_sponsorPredURI           = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#sponsor')
_surnamePredicateURI      = URIRef('http://xmlns.com/foaf/0.1/surname')
_degreePredicateURIPrefix = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#degree')
_employmentActiveURI      = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#employmentActive')
_homePageURI              = URIRef('http://edrn.nci.nih.gov/rdf/schema.rdf#url')

def _transformMemberType(memberType):
    '''Transform a potentially bad member type from the DMCC into a good, clean member type'''
    memberType = memberType.strip()
    if memberType.startswith(u'Associate Member C') or memberType.startswith(u'Assocaite Member C'): # Thanks, DMCC
        return u'Associate Member C'
    elif memberType.startswith(u'Associate Member B'):
        return u'Associate Member B'
    elif memberType == u'Biomarker Developmental  Laboratories': # Thanks, DMCC
        return u'Biomarker Developmental Laboratories'
    elif memberType == u'SPORE':
        return u'SPOREs' # CA-697
    else:
        return memberType
def _transformHomePage(url, ds):
    #when rdf source url does not contain http prefix, homepage url contains rdfsource url
    ds_prefix = "/".join(ds.split('/')[:-1])+"/"
    
    if ds_prefix in url:
        url = url.replace(ds_prefix,"")
        if url.startswith("www."):
            url = "http://"+url
    return url

class SiteFolderIngestor(KnowledgeFolderIngestor):
    '''Site folder ingestion.'''
    def __call__(self, rdfDataSource=None):
        '''Ingest and render a results page.'''
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        if rdfDataSource is None:
            rdfDataSource = context.rdfDataSource
        if not rdfDataSource:
            raise RDFIngestException(_(u'This folder has no RDF data source URL.'))
        normalizerFunction = queryUtility(IIDNormalizer).normalize
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(rdfDataSource))
        statements = self._parseRDF(graph)
        createdObjects = []
        handler = SiteHandler()
        for uri, predicates in statements.items():
            results = catalog(identifier=unicode(uri), object_provides=ISite.__identifier__)
            objectID = handler.generateID(uri, predicates, normalizerFunction)
            #check if homepage URL has rdf datasource in it because of missing http prefix
            if _homePageURI in predicates:
                predicates[_homePageURI][0] = _transformHomePage(predicates[_homePageURI][0], rdfDataSource)
            if len(results) == 1 or objectID in context.keys():
                # Existing site. Update it
                if objectID in context.keys():
                    s = context[objectID]
                else:
                    s = results[0].getObject()
                updateObject(s, uri, predicates, context)
                if _memberTypeURI in predicates and len(predicates[_memberTypeURI]) > 0:
                    s.memberType = _transformMemberType(unicode(predicates[_memberTypeURI][0]))
                # Reset my investigators
                s.setPrincipalInvestigator(None)
                s.setCoPrincipalInvestigators([])
                s.setCoInvestigators([])
                s.setInvestigators([])
                # FIXME:
                # s.manage_delObjects(s.objectIds())
                created = [CreatedObject(s)]
            else:
                if len(results) > 1:
                    # More than one? Nuke 'em all.
                    context.manage_delObjects([s.id for s in results])
                # New site. Create it.
                title = handler.generateTitle(uri, predicates)
                created = handler.createObjects(objectID, title, uri, predicates, statements, context)
            for obj in created:
                obj.reindex()
            createdObjects.extend(created)
        self.objects = createdObjects
        statements, createdSites = self._updateSponsors()
        self._updateSiteIDs(createdSites.values())
        folks = self._ingestPeople()
        warnings = self._updateInvestigators(statements, createdSites, folks)
        for site in createdSites.values():
            site.obj.reindexObject()
        # Set the PI's UID on all members so we can search for everyone who works for his PI'liness
        for createdPerson in folks.itervalues():
            createdPerson.piUID = createdPerson.aq_parent.piUID
        # CA-609: check for sites without any member type
        mailTool = getToolByName(aq_inner(self.context), 'MailHost')
        if mailTool is not None:
            unknowns = ['* %s (%s)' % (i.obj.title, i.obj.siteID) for i in createdSites.values() if not i.obj.memberType]
            if len(unknowns) > 0:
                urlTool = getToolByName(aq_inner(self.context), 'portal_url')
                portal, portalURL = urlTool.getPortalObject(), urlTool()
                src = portal.getProperty('email_from_address', _sa).strip()
                if not src: src = _sa
                charset = portal.getProperty('email_charset', 'utf-8')
                message = _message % {
                    'portalURL':     portalURL,
                    'numberOfSites': len(unknowns),
                    'sitesList':     '\n'.join(unknowns),
                }
                subject = _(u'Notice: the portal ingested some EDRN sites with NO member type')
                try:
                    mailTool.send(message, mto=_na, mfrom=src, subject=subject, charset=charset)
                except (socket.error, smtplib.SMTPException):
                    pass
        self._results = Results(self.objects, warnings)
        return self.renderResults()
    def _updateSiteIDs(self, sites):
        for site in sites:
            identifier = site.identifier
            if not identifier:
                continue
            site.obj.siteID = identifier.split('/')[-1]
    def _updateInvestigators(self, statements, createdSites, createdPeople):
        warnings = []
        for uri, predicates in statements.items():
            site = createdSites[unicode(uri)].obj
            if _piPredicateURI in predicates:
                if (site.identifier, predicates[_piPredicateURI][0]) not in createdPeople:
                    warnings.append(_(
                        u'Primary investigator "${personID}" not found for site "${siteID}"',
                        mapping=dict(personID=predicates[_piPredicateURI][0], siteID=site.identifier)
                    ))
                else:
                    person = createdPeople[(site.identifier, predicates[_piPredicateURI][0])]
                    site.setPrincipalInvestigator(person)
                    site.piUID = person.UID()
                    person.investigatorStatus = 'pi'
                    person.setDescription(u'PI, %s, %s' % (safe_unicode(person.siteName), safe_unicode(person.phone)))
            for predicateURI, fieldName in (
                (_coPIPredicateURI, 'coPrincipalInvestigators'),
                (_coIPredicateURI, 'coInvestigators'),
                (_investigatorPredicateURI, 'investigators')
            ):
                if predicateURI in predicates:
                    people = []
                    for i in predicates[predicateURI]:
                        if (site.identifier, i) not in createdPeople:
                            warnings.append(_(
                                u'Person "${personID}" not found for site "${siteID}"',
                                mapping=dict(personID=i, siteID=site.identifier)
                            ))
                        else:
                            people.append(createdPeople[(site.identifier, i)])
                    if len(people) > 0:
                        # Lovely. Steven Skates is listed twice for Brigham & Womens, as two separate people but with
                        # slightly differently formatted phone numbers. Clearly he's a dupe. However, our ingest of
                        # people deletes any existing "skates-steven", so there's only one as far as the portal's
                        # concerned. As such, we can't set both as an investigator, so take the intersection of the
                        # available staff with the staff that we're trying to set.
                        possibleUIDs = set([site[j].UID() for j in site.objectIds()])
                        setUIDs = set(j.UID() for j in people)
                        mutator = site.schema[fieldName].getMutator(site)
                        mutator(list(setUIDs.intersection(possibleUIDs)))
                        for j in people:
                            if j.investigatorStatus != 'pi': # Don't demote.
                                j.investigatorStatus = 'investigator'
                            j.setDescription(u'Investigator, %s, %s' % (j.siteName, j.phone))
        return warnings
    def _updateSponsors(self):
        context = aq_inner(self.context)
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(context.rdfDataSource))
        statements = self._parseRDF(graph)
        createdSites = dict([(i.identifier, i) for i in self.objects])
        for uri, predicates in statements.items():
            if _sponsorPredURI in predicates:
                uids = getUIDsFromURIs(context, predicates[_sponsorPredURI])
                if len(uids) >= 1:
                    site = createdSites[unicode(uri)]
                    site.obj.setSponsor(uids[0])
        return statements, createdSites
    def _ingestPeople(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        normalizerFunction = queryUtility(IIDNormalizer).normalize
        graph = ConjunctiveGraph()
        graph.parse(URLInputSource(context.peopleDataSource))
        statements = self._parseRDF(graph)
        createdPeople = {}
        for uri, predicates in statements.items():
            persons = catalog(identifier=unicode(uri), object_provides=IPerson.__identifier__)
            person_list = [p.id for p in persons]
            employmentStatus = self._getNameComponent(_employmentActiveURI, predicates)
            if _siteURI not in predicates:
                # Person without a site, ignore him or her.
                continue
            siteURIs = [unicode(i) for i in predicates[_siteURI]]
            results = catalog(object_provides=ISite.__identifier__, identifier=siteURIs)
            if len(results) == 0:
                # Person with a site, but it's unknown, so again, ignore him or her.
                continue
            for site in [i.getObject() for i in results]:
                if employmentStatus == "Former employee":
                    # Person who is not an current employee anymore
                    # make sure to delete them if they exist
                    if len(persons) > 0:
                        for pid in person_list:
                            if pid in site.objectIds():
                                site.manage_delObjects(pid)
                    continue
                objectID = self._generatePersonID(predicates, normalizerFunction)
                if objectID in site.objectIds():
                    site.manage_delObjects(objectID)
                person = site[site.invokeFactory('Person', objectID)]
                updateObject(person, uri, predicates, context)
                person.siteName = site.title
                person.setDescription(u'Staff, %s, %s' % (safe_unicode(person.siteName), safe_unicode(person.phone)))
                person.memberType = site.memberType
                degrees = []
                for degreePredicateURI in [URIRef(_degreePredicateURIPrefix + unicode(i)) for i in range(1, 4)]:
                    if degreePredicateURI in predicates:
                        degree = unicode(predicates[degreePredicateURI][0])
                        degree.strip()
                        if degree:
                            degrees.append(degree)
                person.setDegrees(degrees)
                if _photoPredicateURI in predicates:
                    url = predicates[_photoPredicateURI][0]
                    contentType = mimetypes.guess_type(url)[0] or 'image/gif'
                    try:
                        with contextlib.closing(urllib2.urlopen(url)) as con:
                            field = person.schema['image']
                            field.set(person, con.read(), content_type=contentType, mimetype=contentType)
                    except urllib2.HTTPError:
                        pass
                person.reindexObject()
                createdPeople[(site.identifier, uri)] = person
        return createdPeople
    def _generatePersonTitle(self, uri, predicates):
        '''Given a triple of (last name, first name, middle name), generate an appropriate object title.
        The form is "Last, First Middle" where middle may appear in first if the first is None and
        the comma disappears if both are None.'''
        last, first, middle = self._createNameComponentsFromPredicates(predicates)
        given = first
        if not given:
            given = middle
        else:
            if middle:
                given += ' ' + middle
        if not given:
            return last
        else:
            return '%s, %s' % (last, given)
    def _generatePersonID(self, predicates, normalizerFunction):
        # FIXME
        return normalizerFunction(' '.join(self._createNameComponentsFromPredicates(predicates)))
    def _getNameComponent(self, predicateURI, predicates):
        '''Return a component of a human being's name identified by predicateURI from the
        given set of predicates. If the component is missing, return an empty string.'''
        if predicateURI in predicates:
            return unicode(predicates[predicateURI][0])
        return u''
    def _createNameComponentsFromPredicates(self, predicates):
        '''Return a triple containing (last, first, middle) name components
        of a person. If a part is missing, leave it as None.'''
        return (
            self._getNameComponent(_surnamePredicateURI, predicates),
            self._getNameComponent(_givenNamePredicateURI, predicates),
            self._getNameComponent(_middleNamePredicateURI, predicates)
        )



class SiteHandler(IngestHandler):
    '''Handler for ``Site`` objects.'''
    def createObjects(self, objectID, title, uri, predicates, statements, context):
        s = context[context.invokeFactory('Site', objectID)]
        updateObject(s, uri, predicates, context)
        if _memberTypeURI in predicates and len(predicates[_memberTypeURI]) > 0:
            s.memberType = _transformMemberType(unicode(predicates[_memberTypeURI][0]))
        return [CreatedObject(s)]
    def generateID(self, uri, predicates, normalizerFunction):
        filterer = MarkupFilterer()
        filterer.feed(predicates[_dcTitleURI][0])
        fullTitle = u'%s %s' % (urlparse.urlparse(uri)[2].split('/')[-1], filterer.getResult())
        return normalizerFunction(fullTitle)


registerHandler(_siteTypeURI, SiteHandler())
