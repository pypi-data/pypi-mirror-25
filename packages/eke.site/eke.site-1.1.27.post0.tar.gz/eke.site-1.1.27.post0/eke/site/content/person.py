# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Person.'''

from Acquisition import aq_parent
from eke.knowledge.content import knowledgeobject
from eke.site import ProjectMessageFactory as _
from eke.site.config import PROJECTNAME
from eke.site.interfaces import IPerson, ISite
from eke.site.utils import generateTitleFromNameComponents
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.i18n.normalizer.interfaces import IUserPreferredURLNormalizer
from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from Products.validation import V_REQUIRED
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import queryUtility

PersonSchema = knowledgeobject.KnowledgeObjectSchema.copy() + atapi.Schema((
    atapi.StringField(
        'salutation',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Salutation'),
            description=_(u'Words used to address the person.'),
        ),
        required=False,
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#salutation',
    ),
    atapi.StringField(
        'givenName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Given Name'),
            description=_(u'The name given to the person at birth and is oft considered the "first" name in Western societies.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/givenname',
    ),
    atapi.StringField(
        'middleName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Middle Name'),
            description=_(u'A secondary name given the person.'),
        ),
        required=False,
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#middleName',
    ),
    atapi.StringField(
        'surname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Surname'),
            description=_(u'The family name oft inherited from birth parents and considered the "last" name in Western societies'),
        ),
        required=True,
        predicateURI='http://xmlns.com/foaf/0.1/surname',
    ),
    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Telephone Number'),
            description=_(u'The number at which the person may be reached via the Public Switched Telephone Network.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/phone',
    ),
    atapi.StringField(
        'fax',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'FAX'),
            description=_(u'Facsimile telephone number.'),
        ),
        predicateURI='http://www.w3.org/2001/vcard-rdf/3.0#fax',
    ),
    atapi.TextField(
        'mailingAddress',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Mailing Address'),
            description=_(u'The postal address to which mail may be sent.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#mailingAddress',
    ),
    atapi.TextField(
        'physicalAddress',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Physical Address'),
            description=_(u'The address where the site exists.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#physicalAddress',
    ),
    atapi.TextField(
        'shippingAddress',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Shipping Address'),
            description=_(u'The address where parcels destined for the site may be sent.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#shippingAddress',
    ),
    atapi.StringField(
        'edrnTitle',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'EDRN Title'),
            description=_(u'Title or honorific given by the Early Detection Research Network.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#edrnTitle',
    ),
    atapi.StringField(
        'specialty',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Specialty'),
            description=_(u'Area of specialization taken by this person.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#specialty',
    ),
    atapi.StringField(
        'mbox',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Mail Box Address'),
            description=_(u'The address at which the person may receive electronic mail.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/mbox',
    ),
    atapi.ImageField(
        'image',
        required=False,
        storage=atapi.AnnotationStorage(migrate=True),
        languageIndependent=True,
        max_size=zconf.ATNewsItem.max_image_dimension,
        sizes={
            'large'   : (768, 768),
            'preview' : (400, 400),
            'mini'    : (200, 200),
            'thumb'   : (128, 128),
            'tile'    :  (64, 64),
            'icon'    :  (32, 32),
            'listing' :  (16, 16),
        },
        validators=(('isNonEmptyFile', V_REQUIRED), ('checkNewsImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(
            description=_(u'An image for this person, such as a photograph or mugshot.'),
            label=_(u'Image'),
            show_content_type=False,
        ),
    ),
    atapi.ComputedField(
        'title',
        searchable=True,
        required=False,
        expression='context._computeTitle()',
        accessor='Title',
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'investigatorStatus',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        default='staff',
        widget=atapi.StringWidget(
            label=_(u'Investigator'),
            description=_(u'Status of this person as an investigator or as a mere staff member.'),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'memberType',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        modes=('view',),
        widget=atapi.StringWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'siteName',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        modes=('view',),
        widget=atapi.StringWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'piUID',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        widget=atapi.StringWidget(
            label=_(u'PI UID'),
            description=_(u'Unique identifier of the principal investigator of the site where this person works.'),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'accountName',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Account Name'),
            description=_(u'DMCC-assigned account username. Note that changing this manually has no effect at the DMCC.'),
        ),
        predicateURI='http://xmlns.com/foaf/0.1/accountName',
    ),
    atapi.StringField(
        'secureSiteRole',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Secure Site Role'),
            description=_(u'Role the person plays on the EDRN Secure Site.')
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#secureSiteRole',
    ),
    atapi.LinesField(
        'degrees',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u'Degrees'),
            description=_(u'Academic degrees bestowed on this person'),
        ),
    ),
))

finalizeATCTSchema(PersonSchema, folderish=False, moveDiscussion=False)

class Person(knowledgeobject.KnowledgeObject):
    '''Person.'''
    implements(IPerson)
    schema             = PersonSchema
    portal_type        = 'Person'
    accountName        = atapi.ATFieldProperty('accountName')
    degrees            = atapi.ATFieldProperty('degrees')
    edrnTitle          = atapi.ATFieldProperty('edrnTitle')
    fax                = atapi.ATFieldProperty('fax')
    givenName          = atapi.ATFieldProperty('givenName')
    investigatorStatus = atapi.ATFieldProperty('investigatorStatus')
    mailingAddress     = atapi.ATFieldProperty('mailingAddress')
    mbox               = atapi.ATFieldProperty('mbox')
    memberType         = atapi.ATFieldProperty('memberType')
    middleName         = atapi.ATFieldProperty('middleName')
    phone              = atapi.ATFieldProperty('phone')
    physicalAddress    = atapi.ATFieldProperty('physicalAddress')
    piUID              = atapi.ATFieldProperty('piUID')
    salutation         = atapi.ATFieldProperty('salutation')
    shippingAddress    = atapi.ATFieldProperty('shippingAddress')
    siteName           = atapi.ATFieldProperty('siteName')
    specialty          = atapi.ATFieldProperty('specialty')
    secureSiteRole     = atapi.ATFieldProperty('secureSiteRole')
    surname            = atapi.ATFieldProperty('surname')
    def _computeTitle(self):
        return generateTitleFromNameComponents((self.surname, self.givenName, self.middleName))
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)
    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image
        return super(Person, self).__bobo_traverse__(REQUEST, name)
    def setInformationProvidedBySite(self):
        # Get our parent site obj; if we don't have one (or it's not a site but something weird like portal_factory)
        # then we can't do any updating.
        parent = aq_parent(self)
        if parent is None or not ISite.providedBy(parent): return
        # Update my attributes accordingly
        self.siteName, self.memberType, self.piUID = parent.title, parent.memberType, parent.piUID
    def generateNewId(self):
        if self.accountName:
            request = getattr(self, 'REQUEST', None)
            if request is not None:
                return IUserPreferredURLNormalizer(request).normalize(self.accountName)
            else:
                return queryUtility(IURLNormalizer).normalize(self.accountName)
        else:
            return super(Person, self).generateNewId()

atapi.registerType(Person, PROJECTNAME)

def PersonVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state? Or by a specific site?
    results = catalog(object_provides=IPerson.__identifier__)
    items = {}
    for i in results:
        key = u'%s (%s)' % (i.Title.decode('utf-8'), i.siteID.decode('utf-8'))
        uids = items.get(key, [])
        uids.append(i.UID)
        items[key] = uids
    items = items.items()
    items.sort(lambda a, b: cmp(a[0], b[0]))
    terms = []
    for key, uids in items:
        if len(uids) == 1:
            terms.append(SimpleVocabulary.createTerm(uids[0], uids[0], key))
        else:
            for counter, uid in enumerate(uids):
                newKey = u'{} [{}]'.format(key, counter+1)
                terms.append(SimpleVocabulary.createTerm(uid, uid, newKey))
    return SimpleVocabulary(terms)
directlyProvides(PersonVocabularyFactory, IVocabularyFactory)

def PersonVocabularyWithNoReferenceFactory(context):
    terms = [i for i in PersonVocabularyFactory(context)]
    noReference = u'<no reference>' # FIXME: not i18n
    terms.insert(0, SimpleTerm('', noReference))
    return SimpleVocabulary(terms)
directlyProvides(PersonVocabularyWithNoReferenceFactory, IVocabularyFactory)

def PrincipalInvestigatorVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog(object_provides=IPerson.__identifier__, investigatorStatus='pi')
    items = {}
    for i in results:
        name = i.Title.decode('utf-8')
        if name not in items:
            items[name] = []
        uidsForName = items[name]
        uidsForName.append(i.UID)
    terms = []
    for name, uids in items.iteritems():
        if len(uids) == 1:
            terms.append(SimpleVocabulary.createTerm(uids[0], uids[0], name))
        elif len(uids) > 1:
            for index, uid in enumerate(uids, start=1):
                numberedName = u'{} ({})'.format(name, index)
                terms.append(SimpleVocabulary.createTerm(uid, uid, numberedName))
    terms.sort()
    return SimpleVocabulary(terms)
directlyProvides(PrincipalInvestigatorVocabularyFactory, IVocabularyFactory)

def NotPeonsVocabularyFactory(context):
    peon, notPeon, pi = u'Staff', u'Investigator', u'PI' # FIXME: not i18n
    return SimpleVocabulary.fromItems(((pi, 'pi'), (notPeon, 'investigator'), (peon, 'staff')))
directlyProvides(NotPeonsVocabularyFactory, IVocabularyFactory)

def setSiteInformation(context, event):
    if IPerson.providedBy(context): # should always be true
        context.setInformationProvidedBySite()
