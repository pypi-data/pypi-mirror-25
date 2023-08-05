# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Site: interfaces.
'''

from zope import schema
from zope.container.constraints import contains
from eke.site import ProjectMessageFactory as _
from eke.knowledge.interfaces import IKnowledgeFolder, IKnowledgeObject
from Products.ATContentTypes.interface.image import IImageContent

class ISiteFolder(IKnowledgeFolder):
    '''Site folder.'''
    contains('eke.site.interfaces.ISite')
    peopleDataSource = schema.TextLine(
        title=_(u'People RDF'),
        description=_(u'URL to a source of Resource Description Format data that provides information about registered people.'),
        required=True,
    )
    
class IPerson(IKnowledgeObject, IImageContent):
    '''Person.'''
    salutation = schema.TextLine(
        title=_(u'Saluation'),
        description=_(u'Words used to address the person.'),
        required=False,
    )
    givenName = schema.TextLine(
        title=_(u'Given Name'),
        description=_(u'The name given to the person at birth and is usually considered the "first" name in Western societies.'),
        required=False,
    )
    middleName = schema.TextLine(
        title=_(u'Middle Name'),
        description=_(u'A secondary name given the person.'),
        required=False,
    )
    surname = schema.TextLine(
        title=_(u'Surname'),
        description=_(u'The family name often inherited from birth parents and considered the "last" name in Western societies'),
        required=True,
    )
    phone = schema.TextLine(
        title=_(u'Telephone Number'),
        description=_(u'The number at which the person may be reached via the Public Switched Telephone Network.'),
        required=False,
    )
    fax = schema.TextLine(
        title=_(u'FAX'),
        description=_(u'Facsimile telephone number.'),
        required=False,
    )
    edrnTitle = schema.TextLine(
        title=_(u'EDRN Title'),
        description=_(u'Title or honorific given by the Early Detection Research Network.'),
        required=False,
    )
    specialty = schema.TextLine(
        title=_(u'Specialty'),
        description=_(u'Area of specialization taken by this person.'),
        required=False,
    )
    mbox = schema.TextLine(
        title=_(u'Mail Box Address'),
        description=_(u'The address at which the person may receive electronic mail.'),
        required=False,
    )
    mailingAddress = schema.Text(
        title=_(u'Mailing Address'),
        description=_(u'The postal address to which mail may be sent.'),
        required=False,
    )
    physicalAddress = schema.Text(
        title=_(u'Physical Address'),
        description=_(u'The address where the person is.'),
        required=False,
    )
    shippingAddress = schema.Text(
        title=_(u'Shipping Address'),
        description=_(u'The address where parcels destined for the person may be sent.'),
        required=False,
    )
    investigatorStatus = schema.TextLine(
        title=_(u'Investigator'),
        description=_(u'Status of this person as an investigator or as a mere staff member.'),
        required=False,
    )
    memberType = schema.TextLine(
        title=_(u'Member Type'),
        description=_(u'What particular kind of member site this is.'),
        required=False,
    )
    siteName = schema.TextLine(
        title=_(u'Site Name'),
        description=_(u'Name of the site where this member works.'),
        required=False,
    )
    piUID = schema.TextLine(
        title=_(u'PI UID'),
        description=_(u'Unique identifier of the principal investigator of the site where this person works.'),
        required=False,
    )
    accountName = schema.TextLine(
        title=_(u'Account Name'),
        description=_(u'DMCC-assigned account username.'),
        required=False,
    )
    secureSiteRole = schema.TextLine(
        title=_(u'Secure Site Role'),
        description=_(u'What role this person plays at the EDRN Secure Site'),
        required=False,
    )
    degrees = schema.List(
        title=_(u'Degrees'),
        description=_(u'Academic degrees bestowed upon this person'),
        required=False,
        value_type=schema.TextLine(title=_(u'Degree'), description=_(u'Academic degree bestowed upon this person'))
    )

# Pre-declared so that the "sponsor" field works, see below.
class ISite(IKnowledgeObject):
    pass

class ISite(IKnowledgeObject):
    '''Site.'''
    contains('eke.site.interfaces.IPerson')
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'A short name for the site.'),
        required=False,
    )
    sponsor = schema.Object(
        title=_(u'Sponsoring Site'),
        description=_(u"What site, if any, that sponsors this site's membership in EDRN."),
        required=False,
        schema=ISite, # Requires ISite already declared, see above.
    )
    fundingStartDate = schema.Datetime(
        title=_(u'Funding Start Date'),
        description=_(u'When funding for this site started.'),
        required=False,
    )
    fundingEndDate = schema.Datetime(
        title=_(u'Funding End Date'),
        description=_(u'When funding for this site stopped.'),
        required=False,
    )
    fwaNumber = schema.TextLine(
        title=_(u'FWA Number'),
        description=_(u'The so-called "FWA" number assigned to this site.'),
        required=False,
    )
    specialty = schema.TextLine(
        title=_(u'specialty'),
        description=_(u'What this site is really good at.'),
        required=False,
    )
    homePage = schema.TextLine(
        title=_(u'Home Page'),
        description=_(u"URL to the site's \"home page\" on the new Inter-Net phenomenon known as WWW or World Wide Webb. NOTE:" \
            + " Requires NCSA Mosaic or Inter-Net eXplorer."),
        required=False,
    )
    memberType = schema.TextLine(
        title=_(u'Member Type'),
        description=_(u'What particular kind of member site this is.'),
        required=False,
    )
    historicalNotes = schema.Text(
        title=_(u'Historical Notes'),
        description=_(u'Various notes made by various individuals within EDRN about this EDRN site.'),
        required=False,
    )
    principalInvestigator = schema.Object(
        title=_(u'Principal Investigator'),
        description=_(u'The leading investigator leading EDRN research at this site.'),
        required=False,
        schema=IPerson
    )
    coPrincipalInvestigators = schema.List(
        title=_(u'Co-Principal Investigators'),
        description=_(u'Additional leading principal investigators.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Co-Principal Investigator'),
            description=_(u'Additional leading principal investigator.'),
            schema=IPerson
        )
    )
    coInvestigators = schema.List(
        title=_(u'Co-Investigators'),
        description=_(u'Assistant or associate investigators helping out with EDRN research at the site.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Co-Investigator'),
            description=_(u'Assistant or associate investigator helping out.'),
            schema=IPerson
        )
    )
    investigators = schema.List(
        title=_(u'Investigators'),
        description=_(u'Investigators at the site conducting other research.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Investigator'),
            description=_(u'Investigator at the site conducting other research.'),
            schema=IPerson
        )
    )
    piUID = schema.TextLine(
        title=_(u'PI UID'),
        description=_(u'Unique identifier of the principal investigator.'),
        required=False,
    )
    siteID = schema.TextLine(
        title=_(u'Site ID'),
        description=_(u'DMCC-assigned identifier of the site.'),
        required=False,
    )
    organs = schema.List(
        title=_(u'Organs'),
        description=_(u'Names of the organs on which this site focuses.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Organ'),
            description=_(u'Names of an organ on which this site focuses.'),
        )
    )
    proposal = schema.Text(
        title=_(u'Proposal'),
        description=_(u'Title of the proposal that produced this site (for BDLs only).'),
        required=False,
    )
    