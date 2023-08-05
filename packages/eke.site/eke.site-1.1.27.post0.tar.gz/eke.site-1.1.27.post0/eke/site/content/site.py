# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Site.'''

from eke.knowledge import dublincore
from eke.knowledge.content import knowledgeobject
from eke.site.interfaces import ISite, IPerson
from eke.site import ProjectMessageFactory as _
from eke.site.config import PROJECTNAME
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.ATContentTypes.content.folder import ATFolder

SiteSchema = knowledgeobject.KnowledgeObjectSchema.copy() + ATFolder.schema.copy() + atapi.Schema((
    atapi.StringField(
        'abbreviation',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Abbreviation'),
            description=_(u'A short name for the site.'),
            size=10,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbrevName',
    ),
    atapi.ReferenceField(
        'sponsor',
        enforceVocabulary=True,
        multiValued=False,
        relationship='sponsoredBy',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.site.SitesWithNoReference',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Sponsoring Site'),
            description=_(u"What site, if any, that sponsors this site's membership in EDRN."),
        ),
    ),
    atapi.DateTimeField(
        'fundingStartDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Funding Start Date'),
            description=_(u'When funding for this site started.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#fundStart',
    ),
    atapi.DateTimeField(
        'fundingEndDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Funding End Date'),
            description=_(u'When funding for this site stopped.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#fundEnd',
    ),
    atapi.StringField(
        'fwaNumber',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'FWA Number'),
            description=_(u'The so-called "FWA" number assigned to this site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#fwa',
    ),
    atapi.StringField(
        'specialty',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'specialty'),
            description=_(u'What this site is really good at.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#program',
    ),
    atapi.StringField(
        'homePage',
        storage=atapi.AnnotationStorage(),
        required=False,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_(u'Home Page'),
            description=_(u"URL to the site's \"home page\" on the new Inter-Net phenomenon known as WWW or World Wide Webb. "\
                + "NOTE: Requires NCSA Mosaic or Inter-Net eXplorer."),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#url',
    ),
    atapi.StringField(
        'memberType',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Member Type'),
            description=_(u'What particular kind of member site this is.'),
        ),
    ),
    atapi.TextField(
        'historicalNotes',
        storage=atapi.AnnotationStorage(),
        searchable=True,
        required=False,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u'Historical Notes'),
            description=_(u'Various notes made by various individuals within EDRN about this EDRN site.'),
            rows=15,
            allow_file_upload=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#historicalNotes',
    ),
    atapi.ReferenceField(
        'principalInvestigator',
        storage=atapi.AnnotationStorage(),
        required=False,
        enforceVocabulary=True,
        multiValued=False,
        vocabulary_factory=u'eke.site.PeopleWithNoReference',
        relationship='piForThisSite',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Principal Investigator'),
            description=_(u'Lead investigator conducting EDRN research at this site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#pi',
    ),
    atapi.ReferenceField(
        'coPrincipalInvestigators',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.site.People',
        relationship='coPIsForThisSite',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Co-Principal Investigators'),
            description=_(u'Additional leading principal investigators.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#copi',
    ),
    atapi.ReferenceField(
        'coInvestigators',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.site.People',
        relationship='coisForThisSite',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Co-Investigators'),
            description=_(u'Assistant and associate investigators helping with EDRN research at this site.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#coi',
    ),
    atapi.ReferenceField(
        'investigators',
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'eke.site.People',
        relationship='investigatorsAtThisSite',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Investigators'),
            description=_(u'Investigators at the site conducting other research.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#investigator',
    ),
    atapi.ComputedField(
        'piUID',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        expression='context._computePIUID()',
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'siteID',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Site ID'),
            description=_(u'DMCC-assigned identifier for the site.'),
            size=5,
        ),
    ),
    atapi.LinesField(
        'organs',
        storage=atapi.AnnotationStorage(),
        searchable=True,
        required=False,
        widget=atapi.LinesWidget(
            label=_(u'Organs'),
            description=_(u'Names of the organs on which this site focuses, one per line.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#organ',
    ),
    atapi.TextField(
        'proposal',
        storage=atapi.AnnotationStorage(),
        searchable=True,
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Proposal'),
            description=_(u'Title of the proposal that produced this site (for BDLs only).'),
        ),
    ),
))
# FIXME: KnowledgeObjectSchema has title's predicate set to something wrong.
# When that's finally fixed, remove this line:
SiteSchema['title'].predicateURI = dublincore.TITLE_URI

finalizeATCTSchema(SiteSchema, folderish=True, moveDiscussion=False)

class Site(ATFolder, knowledgeobject.KnowledgeObject):
    '''Site.'''
    implements(ISite)
    schema                   = SiteSchema
    portal_type              = 'Site'
    abbreviation             = atapi.ATFieldProperty('abbreviation')
    coInvestigators          = atapi.ATReferenceFieldProperty('coInvestigators')
    coPrincipalInvestigators = atapi.ATReferenceFieldProperty('coPrincipalInvestigators')
    description              = atapi.ATFieldProperty('description')
    fundingEndDate           = atapi.ATFieldProperty('fundingEndDate')
    fundingStartDate         = atapi.ATFieldProperty('fundingStartDate')
    fwaNumber                = atapi.ATFieldProperty('fwaNumber')
    historicalNotes          = atapi.ATFieldProperty('historicalNotes')
    homePage                 = atapi.ATFieldProperty('homePage')
    investigators            = atapi.ATReferenceFieldProperty('investigators')
    memberType               = atapi.ATFieldProperty('memberType')
    organs                   = atapi.ATFieldProperty('organs')
    piUID                    = atapi.ATFieldProperty('piUID')
    principalInvestigator    = atapi.ATReferenceFieldProperty('principalInvestigator')
    proposal                 = atapi.ATFieldProperty('proposal')
    siteID                   = atapi.ATFieldProperty('siteID')
    specialty                = atapi.ATFieldProperty('specialty')
    sponsor                  = atapi.ATReferenceFieldProperty('sponsor')
    def _computePIUID(self):
        if self.principalInvestigator is not None:
            return self.principalInvestigator.UID()
    def updateMembers(self):
        '''Update my members with any changes made to myself that needs to be propagated to them.'''
        try:
            catalog = getToolByName(self, 'portal_catalog')
        except AttributeError:
            # No catalog means we must still be in the midst of factory-based construction.
            # In that case, we have no child objects to worry about!
            return
        members = catalog(
            object_provides=IPerson.__identifier__,
            path=dict(query='/'.join(self.getPhysicalPath()), depth=1),
        )
        # No members? No need to update anyone
        if len(members) == 0: return
        # First, let's make a table of member UID to member catalog brain
        members = dict([(i.UID, i) for i in members])
        # We'll also need a place to track members we've updated so we can reindex them when we're done
        toReindex = set()
        # First, make sure the illustrious PI is appropriately illuminated
        piUID = self.getRawPrincipalInvestigator()
        if piUID:
            # The PI gets special treatment and gets everything updated
            try:
                o = members[piUID].getObject()
                o.investigatorStatus, o.siteName, o.memberType = 'pi', self.title, self.memberType
                toReindex.add(o)
            except KeyError:
                # In this weird case, we have a PI who's not also a member, possibly moved
                # to another institute (or just bad DMCC data).  In that case, the PI is
                # likely invalid, so clear it.
                self.setPrincipalInvestigator(None)
        # Now, let's gather all of the UIDs of anyone who's an investigator, just not the illustrious PI.
        investigatorUIDs = []
        investigatorUIDs.extend(self.getRawCoPrincipalInvestigators())  # Such as the co-PIs
        investigatorUIDs.extend(self.getRawCoInvestigators())           # And the coIs
        investigatorUIDs.extend(self.getRawInvestigators())             # And the Is
        investigatorUIDs = frozenset(investigatorUIDs)
        # Ensure investigators are flagged
        for uid in investigatorUIDs:
            try:
                b = members[uid]
                if b.investigatorStatus != 'investigator' and b.investigatorStatus != 'pi':
                    o = b.getObject()
                    o.investigatorStatus = 'investigator'
                    toReindex.add(o)
            except KeyError:
                # Another weird case with DMCC data or people shifting about: an investigator
                # who's not on the staff list.  Ignore.
                pass
        # Ensure peons aren't flagged
        for uid in frozenset(members.keys()) - investigatorUIDs:
            b = members[uid]
            if b.investigatorStatus != 'staff' and b.investigatorStatus != 'pi':
                o = b.getObject()
                o.investigatorStatus = 'staff'
                toReindex.add(o)
        # Now make sure everyone's got the right site name, member type, and piUID
        toUpdate = [
            b for b in members.values() if b.siteName.decode('utf-8') != self.title or b.memberType.decode('utf-8') != self.memberType or b.piUID != self.piUID
        ]

        for b in toUpdate:
            o = b.getObject()
            o.siteName, o.memberType, o.piUID = self.title, self.memberType, self.piUID
            toReindex.add(o)
        # Finally, reindex the updated
        for i in toReindex:
            i.reindexObject(idxs=['investigatorStatus', 'siteName', 'memberType', 'piUID'])

atapi.registerType(Site, PROJECTNAME)

def SiteVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state?
    results = catalog(object_provides=ISite.__identifier__, sort_on='sortable_title')
    terms = []
    for i in results:
        displayString = u'{} ({})'.format(i.Title.decode('utf-8'), i.siteID.decode('utf-8'))
        terms.append(SimpleVocabulary.createTerm(i.UID, i.UID, displayString))    
    return SimpleVocabulary(terms)
directlyProvides(SiteVocabularyFactory, IVocabularyFactory)

def SiteVocabularyWithNoReferenceFactory(context):
    terms = [i for i in SiteVocabularyFactory(context)]
    noReference = u'<no reference>' # FIXME: not i18n
    terms.insert(0, SimpleTerm('', noReference))
    return SimpleVocabulary(terms)
directlyProvides(SiteVocabularyWithNoReferenceFactory, IVocabularyFactory)

def SiteNamesVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state?
    class _Site(object):
        def __init__(self, uid, name):
            self.uid, self.name = uid, name
        def __cmp__(self, other):
            return cmp(self.name, other.name)
    results = catalog(object_provides=ISite.__identifier__)
    sites = frozenset([_Site(i.UID, i.Title.decode('utf-8')) for i in results])
    sites = list(sites)
    sites.sort()
    return SimpleVocabulary([SimpleVocabulary.createTerm(i.uid, i.uid, i.name) for i in sites])
directlyProvides(SiteNamesVocabularyFactory, IVocabularyFactory)

def MemberTypeVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    memberTypes = [(i.decode('utf-8'), i.decode('utf-8')) for i in catalog.uniqueValuesFor('memberType')]
    memberTypes.sort()
    return SimpleVocabulary.fromItems(memberTypes)
directlyProvides(MemberTypeVocabularyFactory, IVocabularyFactory)

def updateSiteMembers(context, event):
    if ISite.providedBy(context): # should always be true
        context.updateMembers()
