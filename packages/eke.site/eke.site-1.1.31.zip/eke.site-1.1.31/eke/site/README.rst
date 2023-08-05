This package provides Plone 3 content objects for the EDRN Knowledge
Environment (EKE_)'s management, display, and RDF ingest of participating
sites.  Once a hospital, clinic, research center, university hospital,
university clinic, university research center, think tank, quasi-legal medical
facility, or pharmaceutical plant of questionable morals located on off-shore
platforms in international waters joins the Early Detection Research Network,
we call it a "site".  This component is responsible for managing and easing
discovery of those sites, as well as related information.


Content Types
=============

The content types introduced in this package include the following:

Site Folder
    A folder that contains Sites.  It can also repopulate its
    contents from an RDF data source.  They may also contain Site Folders
    as well, should EDRN decide to do some hierarchical organization.
Site
    A single participating EDRN member site identified by URI_.  Sites may
    contain Investigators.
Person
    A single individual at a site, typically a member of the staff or a more
    important-sounding "investigator".

The remainder of this document demonstrates the content types and RDF ingest
using a series of functional tests.


Tests
=====

First we have to set up some things and login to the site::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

We'll also have a second browser that's unprivileged for some later
demonstrations::

    >>> unprivilegedBrowser = Browser(app)

Now we can check out the new types introduced in this package.


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


Site Folder
~~~~~~~~~~~

A site folder contains sites.  They can be created anywhere in the portal::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='site-folder')
    >>> l.url.endswith('createObject?type_name=Site+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Questionable Sites'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/a'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'questionable-sites' in portal.objectIds()
    True
    >>> f = portal['questionable-sites']
    >>> f.title
    'Questionable Sites'
    >>> f.description
    'This folder is just for functional tests.'
    >>> f.rdfDataSource
    'testscheme://localhost/sites/a'

Site Folders hold Sites as well as other Site Folders.  We'll test adding
Sites below, but let's make sure there's a link to created nested Site
Folders::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> l = browser.getLink(id='site-folder')
    >>> l.url.endswith('createObject?type_name=Site+Folder')
    True


Site
~~~~

A single Site object corresponds with a single real-world EDRN member site;
they may be created only within Site Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

So, let's create one in our above Site Folder::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> l = browser.getLink(id='site')
    >>> l.url.endswith('createObject?type_name=Site')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = 'Platform One'
    >>> browser.getControl(name='description').value = 'Top-secret EDRN research platform.'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/p1'
    >>> browser.getControl(name='abbreviation').value = 'P1'
    >>> from datetime import datetime, timedelta
    >>> today = datetime.now()
    >>> tomorrow = today + timedelta(1)
    >>> browser.getControl(name='fundingStartDate_year').displayValue = [str(today.year)]
    >>> browser.getControl(name='fundingStartDate_month').value = ['%02d' % today.month]
    >>> browser.getControl(name='fundingStartDate_day').value = ['%02d' % today.day]
    >>> browser.getControl(name='fundingEndDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='fundingEndDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='fundingEndDate_day').value = ['%02d' % tomorrow.day]
    >>> browser.getControl(name='fwaNumber').value = 'X-19.6C'
    >>> browser.getControl(name='specialty').value = 'Information extraction through aggressive biomarkers.'
    >>> browser.getControl(name='homePage').value = 'http://blackhelicopters.org/'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='historicalNotes').value = 'Redacted.'
    >>> browser.getControl(name='siteID').value = '123'
    >>> browser.getControl(name='organs:lines').value = 'Anus\nRectum'
    >>> browser.getControl(name='proposal').value = 'Bite me.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'platform-one' in f.objectIds()
    True
    >>> p1 = f['platform-one']
    >>> p1.title
    u'Platform One'
    >>> p1.description
    'Top-secret EDRN research platform.'
    >>> p1.identifier
    'http://cia.gov/edrn/p1'
    >>> (p1.fundingStartDate.year(), p1.fundingStartDate.month(), p1.fundingStartDate.day()) == (today.year, today.month, today.day)
    True
    >>> (p1.fundingEndDate.year(), p1.fundingEndDate.month(), p1.fundingEndDate.day()) == (tomorrow.year, tomorrow.month, tomorrow.day)
    True
    >>> p1.fwaNumber
    'X-19.6C'
    >>> p1.specialty
    'Information extraction through aggressive biomarkers.'
    >>> p1.homePage
    'http://blackhelicopters.org/'
    >>> p1.memberType
    'Biomarker Developmental Laboratories'
    >>> p1.historicalNotes
    'Redacted.'
    >>> p1.siteID
    '123'
    >>> p1.organs
    ('Anus', 'Rectum')
    >>> p1.proposal
    'Bite me.'

A site should automatically make the link to the homepage clickable, so let's
make sure there's an href in there with the address::

    >>> browser.contents
    '...href="http://blackhelicopters.org/"...'

CA-659 says we need to include the site ID::

    >>> browser.contents
    '...Site ID...123...'

One site may sponsor another.  Let's create a second site and have it be
sponsored by our first site::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Platform Two'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/p2'
    >>> browser.getControl(name='memberType').value = 'Biomarker Reference Laboratories'
    >>> browser.getControl('Platform One (123)').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> p2 = f['platform-two']
    >>> p2.sponsor.title
    u'Platform One'

CA-971 notices that sponsoring is required—i.e., the sponsoring site field
defaults to some site and there's no way to make it unset.  Well, that *was*
the case, but notice now::

    >>> browser.getLink('Edit').click()
    >>> browser.contents
    '...Edit...Sponsoring Site...&lt;no reference&gt;...Platform One...Platform Two...'

See?  You can set it to "<no reference>" to mean no sponsoring site.

CA-666 wants sponsors to show up only for associate member sites.  Platform
Two, as created above, is a full Biomarker Reference Lab, and so even though
it's a sponsored site, we need to hide that fact.  Do we?  Checking::

    >>> browser.open(portalURL + '/questionable-sites/platform-two')
    >>> 'Sponsor:' in browser.contents
    False

Good.  But now, let's change Platform Two to the associate type and see if the
sponsorship fact does show up::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='memberType').value = 'Associate Member'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites/platform-two')
    >>> 'Sponsor:' in browser.contents
    True
    >>> browser.contents
    '...Sponsor:...Platform One...'

Perfect.  But now let's put it back::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='memberType').value = 'Biomarker Reference Laboratories'
    >>> browser.getControl(name='form.button.save').click()


Site Folder View
~~~~~~~~~~~~~~~~

The site folder, by default, displays sites ordered by their types.  Checking
that::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.contents
    '...Biomarker Developmental Laboratories...Platform One...Biomarker Reference Laboratories...Platform Two...'

Also, we want a little hyperlink list
(http://oodt.jpl.nasa.gov/jira/browse/CA-400) at the top that lets a user jump
to a certain section of sites::

    >>> browser.contents
    '...href="#bdls"...href="#brls"...'
    >>> browser.contents
    '...name="bdls"...name="brls"...'

CA-728 wanted a specific ordering to that little hyperlink list, regardless of
whether such sites are present in portal.  That ordering should be:

* Biomarker Developmental Laboratories
* Biomarker Reference Laboratories
* Clinical Validation Centers
* Data Management and Coordinating Center
* Informatics Center
* National Cancer Institute
* Associate Members
* SPOREs
* Non-EDRN Sites

Does our little hyperlink list do that?  Let's find out::

    >>> bdl = browser.contents.index('Biomarker Developmental Laboratories')
    >>> brl = browser.contents.index('Biomarker Reference Laboratories')
    >>> cvc = browser.contents.index('Clinical Validation Center')
    >>> dmcc = browser.contents.index('Data Management and Coordinating Center')
    >>> ic = browser.contents.index('Informatics Center')
    >>> nci = browser.contents.index('National Cancer Institute')
    >>> associate = browser.contents.index('Associate Members')
    >>> spore = browser.contents.index('SPOREs')
    >>> nonEDRN = browser.contents.index('Non-EDRN Sites')
    >>> bdl < brl < cvc < dmcc < ic < nci < associate < spore < nonEDRN
    True

We don't have any associate sites yet, so if a user clicked on the little
hyperlink item for Associate Members, she'd get a little admonition::

    >>> browser.contents
    '...Associate Members...There are no associate members...'

Let's go ahead and add one::

    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Hi! I'm an Associate."
    >>> browser.getControl(name='identifier').value = 'http://associate.com/'
    >>> browser.getControl(name='memberType').value = 'Associate Member C2 - Non Funded Former PI'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')

And now::

    >>> browser.contents
    '...Associate Members...Associate Member C...Hi! I\'m an Associate...'

Additionally, any nested site folders should appear above the list of sites::

    >>> 'Special Subsection' not in browser.contents
    True
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Special Subsection on Morally Dubious Sites'
    >>> browser.getControl(name='rdfDataSource').value = 'file:/dev/null'
    >>> browser.getControl(name='peopleDataSource').value = 'file:/dev/null'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.contents
    '...Special Subsection...Platform One...Platform Two...'

CA-667 says that BDLs and CVCs need to show the organ being worshiped at their
site.  For BDLs, there should be a heading for the organ, followed by all the
sites that worship that organ.  For CVCs, we just need a column that shows the
organ.

The site "Platform One" we added above has both "Anus" and "Recutm" as its
organs of worship, and since it's a Biomarker Developmental Laboratory, it
gets an organ heading and, thanks to CA-691, appears under each::

    >>> browser.contents
    '...<h4>Anus</h4>...Platform One...<h4>Rectum</h4>...Platform One...'

Let's add another site that's a Clinical Validation Center (CVC) and see if
its organ shows up in a table row::

    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Platform Seven"
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/platform/7'
    >>> browser.getControl(name='memberType').value = 'Clinical Validation Center'
    >>> browser.getControl(name='organs:lines').value = 'Rectum\nUrethra'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.contents
    '...Platform Seven...<td>Rectum, Urethra</td>...'

Further, the organ should not appear in the site view unless the site is a
BDL or a CVC::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> 'Anus' in browser.contents
    True
    >>> browser.open(portalURL + '/questionable-sites/platform-seven')
    >>> 'Rectum' in browser.contents
    True

Those work, but does the organ appear for say an IC site?  Adding one::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Platform Silly'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/platform/silly'
    >>> browser.getControl(name='memberType').value = 'Informatics Center'
    >>> browser.getControl(name='organs:lines').value = 'Hemorrhoid'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'Hemorrhoid' in browser.contents
    False
    >>> browser.open(portalURL + '/questionable-sites')
    >>> 'Hemorrhoid' in browser.contents
    False

Great.

CA-667 goes onto say that Biomarker Developmental Laboratories should be
grouped together not just under their organs of worship, but then sub-grouped
under their common proposal titles.  So, let's add some more BDLs and see if
they do that::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "BDL One"
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/1'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='organs:lines').value = 'Anal Gland'
    >>> browser.getControl(name='proposal').value = 'Sigh.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "BDL Two"
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/2'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='organs:lines').value = 'Anal Gland'
    >>> browser.getControl(name='proposal').value = 'Sigh.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Another BDL"
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/3'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='organs:lines').value = 'Anal Gland'
    >>> browser.getControl(name='proposal').value = 'Another sigh.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Proposal-less BDL"
    >>> browser.getControl(name='organs:lines').value = 'Anal Gland'
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/4'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Organ-less BDL"
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/4'
    >>> browser.getControl(name='proposal').value = 'Whatevs.'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = "Proposal-less and Organ-less BDL"
    >>> browser.getControl(name='identifier').value = 'http://bdlsrus.com/4'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='form.button.save').click()

OK, now let's see if they're grouped::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.contents
    '...Biomarker Developmental...Sites With No Associated Organ...Proposal-less and Organ-less...(No Proposal)...Organ-less...Whatevs...Anal Gland...Proposal-less...(No Proposal)...Another BDL...Another sigh...BDL One...BDL Two...Sigh...Anus...Platform One...Bite me...Rectum...Platform One...Bite me...'

There.


People
~~~~~~

People work at sites who presumably pay them for their efforts and provide
insurance and perhaps other perks like coffee and a lounge where they can talk
about what happened on *Lost* last night.  To model this, Site objects act as
containers for Person objects.  Person objects cannot be created anywhere but
within Site objects::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='person')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

Inside a Site object is just fine:: 

    >>> import cStringIO, base64
    >>> fakeImage = cStringIO.StringIO(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> l = browser.getLink(id='person')
    >>> l.url.endswith('createObject?type_name=Person')
    True
    >>> l.click()
    >>> browser.getControl(name='description').value = 'The gardener of the east grounds.'
    >>> browser.getControl(name='identifier').value = 'http://my.house/staff/3'
    >>> browser.getControl(name='salutation').value = 'Senor'
    >>> browser.getControl(name='givenName').value = 'Prospero'
    >>> browser.getControl(name='middleName').value = 'Diego'
    >>> browser.getControl(name='surname').value = 'Montoya'
    >>> browser.getControl(name='phone').value = '+1 575 555 5011'
    >>> browser.getControl(name='fax').value = '+1 575 555 5012'
    >>> browser.getControl(name='edrnTitle').value = 'Mojo Gardener'
    >>> browser.getControl(name='specialty').value = 'Pansies'
    >>> browser.getControl(name='mailingAddress').value = 'PO Box 3625, Campus Station, Socorro NM 87801'
    >>> browser.getControl(name='physicalAddress').value = '111 Church Street Socorro NM 87801'
    >>> browser.getControl(name='shippingAddress').value = "Wrap in waterpoof paper and drop off nearby; we'll get it."
    >>> browser.getControl(name='image_file').add_file(fakeImage, 'image/png', 'fakeImage.png')
    >>> browser.getControl(name='mbox').value = 'mailto:pdm87801@aol.com'
    >>> browser.getControl(name='accountName').value = 'kittyfan7122'
    >>> browser.getControl(name='secureSiteRole').value = 'Other Admin Staff'

Notice we haven't set the title.  The object's title should be automatically
generated from the person's names.  Let's submit this form and see if it
works::

    >>> browser.getControl(name='form.button.save').click()
    >>> site = portal['questionable-sites']['platform-one']
    >>> 'kittyfan7122' in site.objectIds()
    True
    >>> pdm = site['kittyfan7122']
    >>> pdm.title
    'Montoya, Prospero Diego'
    >>> pdm.identifier
    'http://my.house/staff/3'
    >>> pdm.description
    'The gardener of the east grounds.'
    >>> pdm.salutation
    'Senor'
    >>> pdm.givenName
    'Prospero'
    >>> pdm.middleName
    'Diego'
    >>> pdm.surname
    'Montoya'
    >>> pdm.phone
    '+1 575 555 5011'
    >>> pdm.fax
    '+1 575 555 5012'
    >>> pdm.edrnTitle
    'Mojo Gardener'
    >>> pdm.specialty
    'Pansies'
    >>> pdm.mailingAddress
    'PO Box 3625, Campus Station, Socorro NM 87801'
    >>> pdm.physicalAddress
    '111 Church Street Socorro NM 87801'
    >>> pdm.shippingAddress
    "Wrap in waterpoof paper and drop off nearby; we'll get it."
    >>> pdm.mbox
    'mailto:pdm87801@aol.com'
    >>> pdm.accountName
    'kittyfan7122'
    >>> pdm.secureSiteRole
    'Other Admin Staff'

Notice how the last name was formatted?  It uses all of the name fields to
generate a title.  However, let's make sure that generation works even when
parts are missing.  First, we'll nuke the middle name::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='middleName').value= ''
    >>> browser.getControl(name='form.button.save').click()
    >>> pdm.title
    'Montoya, Prospero'

And if there's no first name either::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='givenName').value = ''
    >>> browser.getControl(name='form.button.save').click()
    >>> pdm.title
    'Montoya'

Perfect.

Also notice that Mr Montoya has certain other attributes automatically set::

    >>> pdm.siteName
    'Platform One'
    >>> pdm.memberType
    'Biomarker Developmental Laboratories'
    >>> pdm.investigatorStatus
    'staff'

The site name and member type are duplicated from the parent container's
attributes so that we can do high-speed catalog-based searches for individual
people based on those fields.  The flag that indicates whether he's an
investigator defaults to false, until, that is, if he's marked as such at the
site.  Furthermore, the piUID should be unset::

    >>> not pdm.aq_explicit.piUID
    True

Let's update all of those attributes in the Site object and see what happens
to the person.  First, we'll change the name of the site, its type, and we'll
set Mr Montoya as the PI::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'Ex-Platform One'
    >>> browser.getControl(name='memberType').value = 'Silly Development Lab'
    >>> browser.getControl(name='principalInvestigator:list').displayValue = ['Montoya']
    >>> browser.getControl(name='form.button.save').click()

Now check out Mr Montoya::

    >>> pdm.siteName
    'Ex-Platform One'
    >>> pdm.memberType
    'Silly Development Lab'
    >>> pdm.investigatorStatus
    'pi'
    >>> p1.aq_explicit.piUID == pdm.aq_explicit.piUID == pdm.UID()
    True

Woot!  The UID of the PI is set not only in the study but on the person in the
study (who happens to be the PI).  However, let's put things back to normal now::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'Platform One'
    >>> browser.getControl(name='memberType').value = 'Biomarker Developmental Laboratories'
    >>> browser.getControl(name='principalInvestigator:list').displayValue = ['<no reference>']
    >>> browser.getControl(name='form.button.save').click()

Notice this as well: Mr Montoya's object ID was set to his account name.
However, we don't want to show the account name on the view template::

    >>> browser.open(portalURL + '/questionable-sites/platform-one/kittyfan7122')
    >>> 'Account Name' in browser.contents
    False

Good.

But not everyone in EDRN has an account name.  What happens then?  Take a
look::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> browser.getLink(id='person').click()
    >>> browser.getControl(name='description').value = 'The gardener of the west grounds.'
    >>> browser.getControl(name='identifier').value = 'http://my.house/staff/3w'
    >>> browser.getControl(name='givenName').value = 'Harrison'
    >>> browser.getControl(name='middleName').value = 'Roebuck'
    >>> browser.getControl(name='surname').value = 'Blithering'
    >>> browser.getControl(name='mbox').value = 'mailto:brh12993@aol.com'
    >>> browser.getControl(name='form.button.save').click()

This time, there was no account name, so how do we get the object ID?  Check
it out::

    >>> 'blithering-harrison-roebuck' in p1.keys()
    True

No account name means we generate the object ID based on the person's name.

Continuing on...


Sites Page Clean Up
~~~~~~~~~~~~~~~~~~~

CA-666 wants some items (program description, funding start & stop dates, and
the mysterious "FWA" number) removed.  Are they gone?  Let's check.::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> 'Funding Start Date' in browser.contents
    False
    >>> 'Funding End Date' in browser.contents
    False
    >>> '"FWA" Number' in browser.contents
    False

Lookin' good.


Staff Listings
~~~~~~~~~~~~~~

People at a Site should appear on the site's view::

    >>> browser.open(portalURL + '/questionable-sites/platform-one')
    >>> browser.contents
    '...Platform One...Staff...Montoya...'
    
However, certain people can be anointed as being co-investigators::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='coInvestigators:list').displayValue = ['Montoya (123)']
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...Platform One...Co-Investigators...Montoya...'

Or, as CA-468 reminds us, as even more special co-principal investigators::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='coPrincipalInvestigators:list').displayValue = ['Montoya (123)']
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...Platform One...Co-Principal Investigators...Montoya...'

Or as investigators, but not necessarily EDRN investigators::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='investigators:list').displayValue = ['Montoya (123)']
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...Platform One...Investigators...Montoya...'

And the primary investigator may be quite special indeed::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='principalInvestigator:list').displayValue = ['Montoya (123)']
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...Platform One...Principal Investigator...Montoya...Co-Investigators...'
    
Furthermore, the PI is listed in the site folder view::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.contents
    '...Montoya...Platform One...'

And not only is he listed, but CA-401 demanded that his name be a link to his
view page::

    '...href="montoya"...Montoya...Platform One...'

That looks like a hyperlink reference to me.


RDF Ingestion
-------------

Site folders support a URL-callable method that causes them to ingest content
via RDF, just like Knowledge Folders in the ``eke.knowledge`` package, but
with the twist that it has *two* RDF data sources: one for data about sites,
and a second for people at sites.

First, let's make a brand new folder in which to experiment::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = 'Annoying Sites'
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/a'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/annoying-sites/content_status_modify?workflow_action=publish')
    >>> f = portal['annoying-sites']

Ingesting from the two RDF data sources::

    >>> browser.open(portalURL + '/annoying-sites/ingest')
    >>> browser.contents
    '...The following items have been created...Dr Tongue\'s 3D Clinic...'
    >>> f.objectIds()
    ['3d-dr-tongues-3d-clinic']
    >>> site = f['3d-dr-tongues-3d-clinic']
    >>> site.title
    u"Dr Tongue's 3D Clinic"
    >>> site.abbreviation
    '3D'
    >>> site.identifier
    'http://tongue.com/clinic/3d'
    >>> site.siteID
    '3d'
    >>> site.fundingStartDate.year(), site.fundingStartDate.month(), site.fundingStartDate.day()
    (1996, 12, 21)
    >>> site.fundingEndDate.year(), site.fundingEndDate.month(), site.fundingEndDate.day()
    (2010, 11, 6)
    >>> site.fwaNumber
    '3D'
    >>> site.principalInvestigator.title
    'Pawaka, Makin'
    >>> site.coPrincipalInvestigators[0].title
    'Pawaka, Makin'
    >>> site.coInvestigators[0].title
    'Pawaka, Makin'
    >>> site.investigators[0].title
    'Pawaka, Makin'
    >>> site.specialty
    'Moving things toward and away from you rapidly.'
    >>> site.homePage
    'http://tongue.com/clinic/3d'
    >>> site.memberType
    'Silly'
    >>> site.historicalNotes
    'Pre-redacted.'
    >>> site.organs
    ('Anus',)
    >>> site.objectIds()
    ['pawaka-makin']
    >>> person = site['pawaka-makin']
    >>> person.title
    'Pawaka, Makin'
    >>> person.description
    "Investigator, Dr Tongue's 3D Clinic, +61 2 9355 5555"
    >>> person.salutation
    'Bootyful'
    >>> degrees = list(person.degrees)
    >>> degrees.sort()
    >>> degrees
    ['Disco Studies', 'MPH', 'Ph.D.']
    >>> person.givenName
    'Makin'
    >>> person.surname
    'Pawaka'
    >>> person.investigatorStatus
    'pi'
    >>> person.secureSiteRole
    'Co-Investigator'
    >>> person.phone
    '+61 2 9355 5555'
    >>> person.mbox
    'mailto:mp69@aol.com'
    >>> person.fax
    '+61 2 9355 5556'
    >>> person.specialty
    'Strangulation'
    >>> person.edrnTitle
    'The Strangler'
    >>> person.mailingAddress
    '3rd Stall Along\nGrand Central Station\nWashington DC 20011\nUNITED STATES'
    >>> person.physicalAddress
    '4th Stall Along\n790 S Marine Corps Dr\nTamuning Guam 96913\nGUAM'
    >>> person.shippingAddress
    '5th Stall Along\n1, Celenceau St\nLipza Beirut 7C\nLEBANON'
    >>> person.aq_explicit.piUID == person.UID()
    True
    >>> img = person.getImage()
    >>> img.tag()
    '<img src="...annoying-sites/3d-dr-tongues-3d-clinic/pawaka-makin/image" alt="Pawaka, Makin" title="Pawaka, Makin"...'
    >>> img.data
    'GIF89...'

The source ``testscheme://localhost/sites/b`` contains both the strange 3D
clinic above *and* a plainer 2D clinic.  Since ingestion purges existing
objects, we shouldn't get duplicate copies of the the 3D clinic if we ingest
with this new data source URL::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/b'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> objIDs = f.objectIds()
    >>> objIDs.sort()
    >>> objIDs
    ['2d-a-plain-2d-clinic', '3d-dr-tongues-3d-clinic']
    
Further, the 3D clinic is sponsoring the 2D clinic::

    >>> twoD = f['2d-a-plain-2d-clinic']
    >>> twoD.sponsor.title
    u"Dr Tongue's 3D Clinic"

Ah, you saw what I did there, right?  Yeah, I also changed the RDF data source
for people.  That's because the data source for sites happens to include both
a PI and Co-Is, and the people data source contains definitions for those
people.  Let's see if they made it::

    >>> threeD = f['3d-dr-tongues-3d-clinic']
    >>> threeD.principalInvestigator.title
    'Cusexijilomimi, Crystal Hotstuff'
    >>> len(threeD.coInvestigators)
    2
    >>> coINames = [i.title for i in threeD.coInvestigators]
    >>> coINames.sort()
    >>> coINames
    ['Cusexijilomimi, Crystal Hotstuff', 'Pawaka, Makin']

Note also that all of these people have the UID of the PI (Ms Makin Pawaka)::

    >>> for objID in threeD.objectIds():
    ...     personObj = threeD[objID]
    ...     personObj.aq_explicit.piUID == threeD.piUID
    True
    True

While we're here, let's check http://oodt.jpl.nasa.gov/jira/browse/CA-483,
which says that site lists should be sorted by investigator names::

    >>> browser.getLink('View').click()
    >>> browser.contents
    '...Alottaspank...Cusexijilomimi...'

That's correct.

The issue http://oodt.jpl.nasa.gov/jira/browse/CA-410 says that the EDRN title
and specialty aren't getting populated.  Let's check that::

    >>> pi = threeD.principalInvestigator
    >>> pi.edrnTitle
    'Hot Stuff'
    >>> pi.specialty
    'Tossed Salads'

The issue http://oodt.jpl.nasa.gov/jira/browse/CA-402 says that a site's
"program description" isn't appearing.  Seriously?  Let's find out.

Better yet, let's not: CA-666 (see above) said to remove the program
description!


Multiple Sites in Different Roles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In http://oodt.jpl.nasa.gov/jira/browse/CA-392, we noticed that a site like
Fred Hutchinson Cancer Research Center appears only once in the portal, even
though it appears almost a dozen times in the RDF (it plays multiple roles,
and each counts as a separate "site").  Let's see if that's fixed.  First,
we'll create a new site folder::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = 'Duplicate Sites'
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/c'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> f = portal['duplicate-sites']

The data source testscheme://localhost/sites/c contains three entries with all
the same name but different URIs.  Let's ingest it::

    >>> browser.getLink('Ingest').click()

We should have three entries::

    >>> len(f.objectIds())
    3


HTML Markup
~~~~~~~~~~~

http://oodt.jpl.nasa.gov/jira/browse/CA-472 revealed that RDF from the DMCC
doesn't contain plain text, but HTML markup.  Sigh.  Let's see if we deal with
that appropriately.  This new data source contains some nasty markup::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/d'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/many'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> browser.open(portalURL + '/duplicate-sites/5d-were-marked-up')
    >>> "We're Marked Up" in browser.contents
    True
    >>> "We're <em>Marked</em> Up" not in browser.contents
    True
    >>> '<em>Marked</em>Up' in browser.contents
    True


Elevating the Investigators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Issue CA-468 wasn't quite satisfied to have the co-investigators appearing
correctly.  It felt that the investigators are so much more highly elevated
than the mere peons at a site, even though they are part of the staff, that
they must never appear *with* the staff.  It just so happens that the "Marked
Up" site from above has a huge staff.  Let's make sure the peons aren't
mingling with the investigators::

    >>> browser.open(portalURL + '/duplicate-sites/5d-were-marked-up')
    >>> import re
    >>> re.match(r'^.+Principal.+Amber.+Co-Principal.+Grail.+Co-Investigators.+Jackal.+Other.+Quake.+Staff.+Graveguard.+Ravenwitch.+Steeldevil.+$', browser.contents, re.DOTALL) is not None
    True

Looks like no caviar will be wasted at this site!


Inconsistent Data
~~~~~~~~~~~~~~~~~

Sometimes data from the DMCC isn't consistent with itself.  CA-571 describes a
specific case where a site (#303) said it had a principal investigator #2101,
who wasn't anywhere in the people RDF.  But we've got deadlines, dammit!  We
can't wait for the DMCC to fix what their own table constraints shouldn't have
allowed in the first place.  So, let's see if we can ingest inconsistent data.

It just so happens that the marked up example from above includes a reference
to an investigator who doesn't exist.  So, we've already demonstrated that the
ingest is resilient to that kind of data.  But, did it warn us about the
problem?  Let's re-ingest and check::

    >>> browser.open(portalURL + '/duplicate-sites/ingest')
    >>> browser.contents
    '...Some unusual things transpired during ingestion...Person "http://nonexistent.com/fake/investigator/who/is/not/real" not found for site "http://html.com/markup/5d"...'

Perfect.


Ordering of Miscellaneous Site Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While CA-483 mandated that sites be ordered by the PI's name, CA-610 says that
doesn't apply to miscellaneous sites.  For those sites only, we should sort by
the site name.  Sigh.  Whatever.  Let's make a new folder and get a metric
crapload of sites loaded (the mail host reset will make sense in the next
section)::

    >>> portal.MailHost.resetSentMessages()
    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Many, many sites'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/many'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/many'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()

That RDF source contains 26 sites.  13 are of the preferred type, like
Biomarker Reference Laboratories, but the other 13 are all of non-preferred,
miscellaneous types.  How are those other 13 ordered?  First up, the Silly
sites:::

    >>> browser.open(portalURL + '/many-many-sites')
    >>> browser.contents
    '...Non-EDRN Sites...Silly...november...oscar...papa...quebec...'

Now, the Foolish sites:::

    >>> browser.contents
    '...Non-EDRN Sites...Foolish...romeo...sierra...tango...uniform...'
    
Now the Rash sites::

    >>> browser.contents
    '...Non-EDRN Sites...Rash...victor...whiskey...x-ray...'

And the lone Stupendous site::

    >>> browser.contents
    '...Non-EDRN Sites...Stupendous...zulu...'

Looks good.


Preservation of Locally-Modified Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CA-667 wants new fields (organ names and proposal text) on sites, however the
RDF data source doesn't provide that information.  So, Heather Kincaid said
she'd fill in that information by hand by logging into the portal and using
Plone's fabulous editing capabilities.  However, one question does arise: will
the automated nightly ingest of RDF data wipe out her changes?

Let's find out.  First, let's make a Site Folder and ingest from a specific
RDF source::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u"Don't Overwrite Me, Bro!"
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/sample'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/sample'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()

Notice the one sample site::

    >>> sample = portal['dont-overwrite-me-bro']['sample-sample']
    >>> sample.proposal
    ''
    >>> sample.organs
    ()

They're blank.  But we'll fix that with a quick edit::

    >>> browser.open(portalURL + '/dont-overwrite-me-bro/sample-sample/edit')
    >>> browser.getControl(name='proposal').value = u'Bite my shiny metal booty.'
    >>> browser.getControl(name='organs:lines').value = u'The Rectum'
    >>> browser.getControl(name='form.button.save').click()

And the values now::

    >>> sample.proposal
    'Bite my shiny metal booty.'
    >>> sample.organs
    ('The Rectum',)

OK, now we'll re-ingest on that folder and check if those edits were preserved::

    >>> browser.open(portalURL + '/dont-overwrite-me-bro/ingest')
    >>> sample = portal['dont-overwrite-me-bro']['sample-sample']
    >>> sample.proposal
    'Bite my shiny metal booty.'
    >>> sample.organs
    ('The Rectum',)

Perfect.


Type B and Type C
~~~~~~~~~~~~~~~~~

In the RDF data provided by the DMCC, there are a certain number of sites that
have the following membership types:

* Associate Member A - EDRN Funded
* Associate Member B1 - EDRN Funded
* Associate Member B2 - Protocol/Project Funded
* Associate Member C1 - Non Funded Applicant
* Assocaite Member C2 - Non Funded Former PI

Note the misspelled "Assocaite".  That is *exactly* how it appears in the
DMCC's data.  Heather wants the B1 and B2 sites grouped together under a
single "B" heading, and the C1 and C2 sites under a single "C" heading,
misspelled or not.  The fun never ends.  Let's create a bunch::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Misspelled Sites'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/many'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/many'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type A Site'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-a/1'
    >>> browser.getControl(name='memberType').value = 'Associate Member A - EDRN Funded'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'A Silly Type Of Site'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/silly/1'
    >>> browser.getControl(name='memberType').value = 'Abandoned'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type B1 Site'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-b1/1'
    >>> browser.getControl(name='memberType').value = 'Associate Member B1 - EDRN Funded'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type B2 Site'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-b2/1'
    >>> browser.getControl(name='memberType').value = 'Associate Member B2 - Protocol/Project Funded'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type C1 Site'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-c1/1'
    >>> browser.getControl(name='memberType').value = 'Associate Member C1 - Non Funded Applicant'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type C2 Misspelled'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-c2/1'
    >>> browser.getControl(name='memberType').value = 'Assocaite Member C2 - Non Funded Former PI'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Type C2 Correctly Spelled'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/type-c2/1'
    >>> browser.getControl(name='memberType').value = 'Associate Member C2 - Non Funded Former PI'
    >>> browser.getControl(name='form.button.save').click()
    
We should list the B's and C's together::

    >>> browser.open(portalURL + '/misspelled-sites')
    >>> browser.contents
    '...Associate Member A...Type A...Associate Member B...Type B1...Type B2...Associate Member C...Type C1...Type C2...Abandoned...Silly...'
    >>> 'Associate Member B1' in browser.contents
    False
    >>> 'Associate Member B2' in browser.contents
    False
    >>> 'Associate Member C1' in browser.contents
    False
    >>> 'Associate Member C2' in browser.contents
    False
    >>> 'Assocaite Member C2' in browser.contents
    False

So far so good.  However, CA-693 wants the abbreviated names to appear in the
nifty new Members List as well.  To pull that off, we need to actually
transform the names on ingest.  Did that happen?  Let's see if sites get
mangled on ingest by creating yet another site folder and ingesting into it::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Mangled Sites'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/mangled'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/empty'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> f = portal['mangled-sites']
    >>> f['b1-associate-member-b1-edrn-funded'].memberType
    'Associate Member B'
    >>> f['b2-associate-member-b2-protocol-project-funded'].memberType
    'Associate Member B'
    >>> f['c1-associate-member-c1-non-funded-applicant'].memberType
    'Associate Member C'
    >>> f['c2-assocaite-member-c2-non-funded-former-pi'].memberType
    'Associate Member C'

Woot.
    

Unknown Types of Sites
~~~~~~~~~~~~~~~~~~~~~~

According to https://oodt.jpl.nasa.gov/jira/browse/CA-609, we need to be
vigilant against sites with an unknown or otherwise unset member type.  The
issue says this should be resolved in the portal, even if the RDF server seems
like a better place for it.  (Ours is not to wonder why, etc.)

It just so happened that the ingest from the above section included one site
whose member type wasn't set: site "yankee".  Did that site make it in?  Let's
take a look at the browser's page once more::

    >>> 'yankee' not in browser.contents
    True

That's all well and nice, but issue CA-609 says we also need to notify the
DMCC whenever we ingest unknown member types.  Did we do that?  Let's check::

    >>> from zope.component import getSiteManager, getUtility
    >>> from Products.MailHost.interfaces import IMailHost
    >>> siteManager = getSiteManager(portal)
    >>> mailHost = siteManager.getUtility(IMailHost)
    >>> sent = mailHost.getSentMessages()
    >>> len(sent)
    1
    >>> sent[0]
    u'(This is an automated message from the EDRN Portal at http://nohost/plone.)\n\nDuring ingest of EDRN member sites, some sites (1, to be exact) had no member type.\n\nThese are the sites that had this problem:\n\n* yankee (yankee)'


Clinical Validation Centers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We sadly don't have a controlled vocabulary for EDRN site member types, which
leads to lots of issues like the extra space between words in
"Biomarker+Developmental++Laboratories" or the misspelled "Assocaite".  Well,
it also leads Heather to think that "Clinical Validation Center" is wrong even
though that's what appears in the DMCC's database.  She wants "Clinical
Validation Centers" (plural) instead, and even filed issue CA-680 to make it
happen.

Does it happen?  First, let's make a site folder and add a Clinical Validation
Center (singular) to it::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Pluralized'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/many'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/many'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Some Lame CVC'
    >>> browser.getControl(name='identifier').value = 'http://sassygrass.org/edrn/cvcs/1'
    >>> browser.getControl(name='memberType').value = 'Clinical Validation Center'
    >>> browser.getControl(name='form.button.save').click()

Now we view the folder::

    >>> browser.open(portalURL + '/pluralized')
    >>> browser.contents
    '...Clinical Validation Centers...Some Lame CVC...'

Wonderful. CA-680 is fixed.


Person De-Duplication
~~~~~~~~~~~~~~~~~~~~~

When a PI is a PI of more than one site, Dan doesn't want us to duplicate the
person object, but instead of the second site refer to the first.  Our code
already supports most of that, but there's an issue when viewing a site whose
PI belongs elsewhere.  That's CA-1029; is it fixed?  Let's make a site and set
the PI to someone from another site altogether::

    >>> browser.open(portalURL + '/questionable-sites')
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'Outsourced PI Site'
    >>> browser.getControl(name='description').value = 'This site has an external principal investigator.'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/outsourced'
    >>> browser.getControl(name='abbreviation').value = 'OS'
    >>> browser.getControl(name='principalInvestigator:list').displayValue = ['Montoya']
    >>> browser.getControl(name='form.button.save').click()

Now, viewing it::

    >>> browser.open(portalURL + '/questionable-sites/outsourced-pi-site')
    >>> browser.contents
    '...Outsourced PI Site...Montoya...'

Looks great!


SPORE
~~~~~

No, it's not a dispersal-based biological structure for reproduction, nor the
video game.  It's CA-697.  The heading over "SPORE" sites should be "SPOREs".
OK, creating a new Sites folder and adding a SPORE site::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'CA-697'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/sites/many'
    >>> browser.getControl(name='peopleDataSource').value = u'testscheme://localhost/people/many'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='site').click()
    >>> browser.getControl(name='title').value = 'A Spore Site'
    >>> browser.getControl(name='identifier').value = 'http://sassygrass.org/edrn/spore/1'
    >>> browser.getControl(name='memberType').value = 'SPORE'
    >>> browser.getControl(name='form.button.save').click()

Now we view the folder::

    >>> browser.open(portalURL + '/ca-697')
    >>> browser.contents
    '...SPOREs...A Spore Site...'


People Moving Between Sites
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apparently if a person moves between sites, you can't manually add any new sites::

    >>> browser.open(portalURL + '/annoying-sites')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/b'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/moved'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> browser.open(portalURL + '/annoying-sites')
    >>> browser.getLink(id='site').click()
    >>> "We're sorry" in browser.contents
    False

No error anymore.


Unicode Dammit
~~~~~~~~~~~~~~

CA-1234 revealed a UnicodeDecodeError from a new EDRN site in Chile::

    >>> browser.open(portalURL + '/annoying-sites')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/chile/sites'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/chile/people'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> "We're sorry" in browser.contents
    False

No error anymore.



RDF Data Sources
~~~~~~~~~~~~~~~~

The URL to an RDF data source is nominally displayed on a knowledge folder::

    >>> browser.open(portalURL + '/many-many-sites')
    >>> browser.contents
    '...RDF Data Source...testscheme://localhost/sites/many...People Data Source...testscheme://localhost/people/many...'

That shows up because we're logged in as an administrator.  Mere mortals
shouldn't see that::

    >>> unprivilegedBrowser.open(portalURL + '/annoying-sites')
    >>> 'RDF Data Source' not in unprivilegedBrowser.contents
    True

That's it!


.. References:
.. _EKE: http://cancer.jpl.nasa.gov/documents/applications/knowledge-environment
.. _RDF: http://w3.org/RDF/
.. _URI: http://w3.org/Addressing/
