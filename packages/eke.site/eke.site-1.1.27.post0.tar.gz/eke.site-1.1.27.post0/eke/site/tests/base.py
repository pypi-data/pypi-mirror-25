# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
Testing base code.
'''

import base64, logging
import eke.knowledge.tests.base as ekeKnowledgeBase

_logger = logging.getLogger('Plone')

_singlePersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:_5="http://www.w3.org/2001/vcard-rdf/3.0#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/1">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_4:salutation>Bootyful</_4:salutation>
    <_4:degree1>Ph.D.</_4:degree1>
    <_4:degree2>MPH</_4:degree2>
    <_4:degree3>Disco Studies</_4:degree3>
    <_3:surname>Pawaka</_3:surname>
    <_3:givenname>Makin</_3:givenname>
    <_3:phone>+61 2 9355 5555</_3:phone>
    <_3:mbox>mailto:mp69@aol.com</_3:mbox>
    <_5:fax>+61 2 9355 5556</_5:fax>
    <_4:specialty>Strangulation</_4:specialty>
    <_4:edrnTitle>The Strangler</_4:edrnTitle>
    <_4:mailingAddress>3rd Stall Along\nGrand Central Station\nWashington DC 20011\nUNITED STATES</_4:mailingAddress>
    <_4:physicalAddress>4th Stall Along\n790 S Marine Corps Dr\nTamuning Guam 96913\nGUAM</_4:physicalAddress>
    <_4:shippingAddress>5th Stall Along\n1, Celenceau St\nLipza Beirut 7C\nLEBANON</_4:shippingAddress>
    <_3:img>testscheme://localhost/people/the-strangler.png</_3:img>
    <_4:secureSiteRole>Co-Investigator</_4:secureSiteRole>
    <_4:employmentActive>Active employee</_4:employmentActive>
  </rdf:Description>
</rdf:RDF>'''

_singleFormerPersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:_5="http://www.w3.org/2001/vcard-rdf/3.0#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/1">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_4:salutation>Bootyful</_4:salutation>
    <_4:degree1>Ph.D.</_4:degree1>
    <_4:degree2>MPH</_4:degree2>
    <_4:degree3>Disco Studies</_4:degree3>
    <_3:surname>Pawaka</_3:surname>
    <_3:givenname>Makin</_3:givenname>
    <_3:phone>+61 2 9355 5555</_3:phone>
    <_3:mbox>mailto:mp69@aol.com</_3:mbox>
    <_5:fax>+61 2 9355 5556</_5:fax>
    <_4:specialty>Strangulation</_4:specialty>
    <_4:edrnTitle>The Strangler</_4:edrnTitle>
    <_4:mailingAddress>3rd Stall Along\nGrand Central Station\nWashington DC 20011\nUNITED STATES</_4:mailingAddress>
    <_4:physicalAddress>4th Stall Along\n790 S Marine Corps Dr\nTamuning Guam 96913\nGUAM</_4:physicalAddress>
    <_4:shippingAddress>5th Stall Along\n1, Celenceau St\nLipza Beirut 7C\nLEBANON</_4:shippingAddress>
    <_3:img>testscheme://localhost/people/the-strangler.png</_3:img>
    <_4:secureSiteRole>Co-Investigator</_4:secureSiteRole>
    <_4:employmentActive>Former employee</_4:employmentActive>
  </rdf:Description>
</rdf:RDF>'''

_doublePersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/1">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Pawaka</_3:surname>
    <_3:givenname>Makin</_3:givenname>
    <_3:phone>+61 2 9355 5555</_3:phone>
    <_3:mbox>mailto:mp69@aol.com</_3:mbox>
    <_4:employmentActive>Current employee</_4:employmentActive>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/2">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Cusexijilomimi</_3:surname>
    <_4:middleName>Hotstuff</_4:middleName>
    <_3:givenname>Crystal</_3:givenname>
    <_3:phone>+61 2 9355 5556</_3:phone>
    <_3:mbox>mailto:chc69@aol.com</_3:mbox>
    <_4:edrnTitle>Hot Stuff</_4:edrnTitle>
    <_4:specialty>Tossed Salads</_4:specialty>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/3">
    <_4:site rdf:resource="http://plain.com/2d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Alottaspank</_3:surname>
    <_3:givenname>Dirk</_3:givenname>
    <_3:phone>+62 2 9355 5556</_3:phone>
    <_3:mbox>mailto:drs69@aol.com</_3:mbox>
    <_4:employmentActive>Current employee</_4:employmentActive>
  </rdf:Description>
</rdf:RDF>'''

_doubleFormerPersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/1">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Pawaka</_3:surname>
    <_3:givenname>Makin</_3:givenname>
    <_3:phone>+61 2 9355 5555</_3:phone>
    <_3:mbox>mailto:mp69@aol.com</_3:mbox>
    <_4:employmentActive>Current employee</_4:employmentActive>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/2">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Cusexijilomimi</_3:surname>
    <_4:middleName>Hotstuff</_4:middleName>
    <_3:givenname>Crystal</_3:givenname>
    <_3:phone>+61 2 9355 5556</_3:phone>
    <_3:mbox>mailto:chc69@aol.com</_3:mbox>
    <_4:edrnTitle>Hot Stuff</_4:edrnTitle>
    <_4:specialty>Tossed Salads</_4:specialty>
    <_4:employmentActive>Former employee</_4:employmentActive>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/3">
    <_4:site rdf:resource="http://plain.com/2d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Alottaspank</_3:surname>
    <_3:givenname>Dirk</_3:givenname>
    <_3:phone>+62 2 9355 5556</_3:phone>
    <_3:mbox>mailto:drs69@aol.com</_3:mbox>
  </rdf:<_4:employmentActive>Current employee</_4:employmentActive>
    Description>
</rdf:RDF>'''

_movedPersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/1">
    <_4:site rdf:resource="http://tongue.com/clinic/3d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Pawaka</_3:surname>
    <_3:givenname>Makin</_3:givenname>
    <_3:phone>+61 2 9355 5555</_3:phone>
    <_3:mbox>mailto:mp69@aol.com</_3:mbox>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/2">
    <_4:site rdf:resource="http://plain.com/2d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Cusexijilomimi</_3:surname>
    <_4:middleName>Hotstuff</_4:middleName>
    <_3:givenname>Crystal</_3:givenname>
    <_3:phone>+61 2 9355 5556</_3:phone>
    <_3:mbox>mailto:chc69@aol.com</_3:mbox>
    <_4:edrnTitle>Hot Stuff</_4:edrnTitle>
    <_4:specialty>Tossed Salads</_4:specialty>
  </rdf:Description>
  <rdf:Description rdf:about="http://pimpmyho.com/data/registered-person/3">
    <_4:site rdf:resource="http://plain.com/2d"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Alottaspank</_3:surname>
    <_3:givenname>Dirk</_3:givenname>
    <_3:phone>+62 2 9355 5556</_3:phone>
    <_3:mbox>mailto:drs69@aol.com</_3:mbox>
  </rdf:Description>
</rdf:RDF>'''


_singleSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://tongue.com/clinic/3d">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Dr Tongue's 3D Clinic</_4:title>
        <_3:abbrevName>3D</_3:abbrevName>
        <_3:fundStart rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1996-12-21T00:00:00</_3:fundStart>
        <_3:fundEnd rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2010-11-06T00:00:00</_3:fundEnd>
        <_3:fwa>3D</_3:fwa>
        <_3:program>Moving things toward and away from you rapidly.</_3:program>
        <_3:url>http://tongue.com/clinic/3d</_3:url>
        <_3:pi rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:coi rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:copi rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:investigator rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:staff rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:memberType>Silly</_3:memberType>
        <_3:historicalNotes>Pre-redacted.</_3:historicalNotes>
        <_3:mailAddr1>3rd Stall Along</_3:mailAddr1>
        <_3:mailAddr2>Grand Central Station</_3:mailAddr2>
        <_3:mailCity>Washington</_3:mailCity>
        <_3:mailState>DC</_3:mailState>
        <_3:mailZip>20011</_3:mailZip>
        <_3:mailCountry>UNITED STATES</_3:mailCountry>
        <_3:physAddr1>4th Stall Along</_3:physAddr1>
        <_3:physAddr2>790 S Marine Corps Dr</_3:physAddr2>
        <_3:physCity>Tamuning</_3:physCity>
        <_3:physState>Guam</_3:physState>
        <_3:physZip>96913</_3:physZip>
        <_3:physCountry>GUAM</_3:physCountry>
        <_3:shipAddr1>5th Stall Along</_3:shipAddr1>
        <_3:shipAddr2>1, Celenceau St</_3:shipAddr2>
        <_3:shipCity>Lipza</_3:shipCity>
        <_3:shipState>Beirut</_3:shipState>
        <_3:shipZip>7C</_3:shipZip>
        <_3:shipCountry>LEBANON</_3:shipCountry>
        <_3:organ>Anus</_3:organ>
    </rdf:Description>
</rdf:RDF>
'''

_doubleSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://tongue.com/clinic/3d">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Dr Tongue's 3D Clinic</_4:title>
        <_3:abbrevName>3D</_3:abbrevName>
        <_3:fundStart rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1996-12-21T00:00:00</_3:fundStart>
        <_3:fundEnd rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2010-11-06T00:00:00</_3:fundEnd>
        <_3:fwa>3D</_3:fwa>
        <_3:pi rdf:resource="http://pimpmyho.com/data/registered-person/2"/>
        <_3:coi rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:coi rdf:resource="http://pimpmyho.com/data/registered-person/2"/>
        <_3:copi rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:investigator rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:staff rdf:resource="http://pimpmyho.com/data/registered-person/1"/>
        <_3:program>Moving things toward and away from you rapidly.</_3:program>
        <_3:url>http://tongue.com/clinic/3d</_3:url>
        <_3:memberType>Silly</_3:memberType>
        <_3:historicalNotes>Pre-redacted.</_3:historicalNotes>
        <_3:mailAddr1>3rd Stall Along</_3:mailAddr1>
        <_3:mailAddr2>Grand Central Station</_3:mailAddr2>
        <_3:mailCity>Washington</_3:mailCity>
        <_3:mailState>DC</_3:mailState>
        <_3:mailZip>20011</_3:mailZip>
        <_3:mailCountry>UNITED STATES</_3:mailCountry>
        <_3:physAddr1>4th Stall Along</_3:physAddr1>
        <_3:physAddr2>790 S Marine Corps Dr</_3:physAddr2>
        <_3:physCity>Tamuning</_3:physCity>
        <_3:physState>Guam</_3:physState>
        <_3:physZip>96913</_3:physZip>
        <_3:physCountry>GUAM</_3:physCountry>
        <_3:shipAddr1>5th Stall Along</_3:shipAddr1>
        <_3:shipAddr2>1, Celenceau St</_3:shipAddr2>
        <_3:shipCity>Lipza</_3:shipCity>
        <_3:shipState>Beirut</_3:shipState>
        <_3:shipZip>7C</_3:shipZip>
        <_3:shipCountry>LEBANON</_3:shipCountry>
    </rdf:Description>
    <rdf:Description rdf:about="http://plain.com/2d">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>A Plain 2D Clinic</_4:title>
        <_3:pi rdf:resource="http://pimpmyho.com/data/registered-person/3"/>
        <_3:sponsor rdf:resource="http://tongue.com/clinic/3d"/>
        <_3:memberType>Silly</_3:memberType>
    </rdf:Description>
</rdf:RDF>'''

_sampleSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://samples.com/samples/sites/sample">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Sample</_4:title>
        <_3:memberType>Sample</_3:memberType>
    </rdf:Description>
</rdf:RDF>'''

_samplePersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:_3="http://xmlns.com/foaf/0.1/"
   xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:_5="http://www.w3.org/2001/vcard-rdf/3.0#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="http://samples.com/samples/sites/sample/staff/p1">
    <_4:site rdf:resource="http://samples.com/samples/sites/sample"/>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <_3:surname>Sampleton</_3:surname>
    <_3:givenname>Joe</_3:givenname>
    <_3:phone>+62 3 4 5555</_3:phone>
    <_3:mbox>mailto:sampleton@samples.com</_3:mbox>
    <_4:specialty>Prestidigitation</_4:specialty>
    <_4:edrnTitle>The Magician</_4:edrnTitle>
  </rdf:Description>
</rdf:RDF>'''

_duplicateSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="http://edrn.nci.nih.gov/data/sites/1">
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
    <_4:title>Gah the Ogre's Site</_4:title>
  </rdf:Description>
  <rdf:Description rdf:about="http://edrn.nci.nih.gov/data/sites/2">
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
    <_4:title>Gah the Ogre's Site</_4:title>
  </rdf:Description>
  <rdf:Description rdf:about="http://edrn.nci.nih.gov/data/sites/3">
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
    <_4:title>Gah the Ogre's Site</_4:title>
  </rdf:Description>
</rdf:RDF>'''

_markedUpSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://html.com/markup/5d">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>We&amp;#39;re &lt;em&gt;Marked&lt;/em&gt; Up</_4:title>
        <_3:abbrevName>&lt;em&gt;Marked&lt;/em&gt;Up</_3:abbrevName>
        <_3:fwa>&#x2014;</_3:fwa>
        <_3:program>Moving &lt;em&gt;things&lt;/em&gt; toward and away from you rapidly.</_3:program>
        <_3:historicalNotes>Ancient &lt;em&gt;stuff&lt;/em&gt; and stuff.</_3:historicalNotes>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_3:coi rdf:resource="http://html.com/markup/5d/personnel/coi"/>
        <_3:copi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_3:investigator rdf:resource="http://html.com/markup/5d/personnel/investigator"/>
        <_3:investigator rdf:resource="http://nonexistent.com/fake/investigator/who/is/not/real"/>
        <_3:staff rdf:resource="http://html.com/markup/5d/personnel/peons/1"/>
        <_3:staff rdf:resource="http://html.com/markup/5d/personnel/peons/2"/>
        <_3:staff rdf:resource="http://html.com/markup/5d/personnel/peons/3"/>
    </rdf:Description>
</rdf:RDF>'''

_manyPeopleRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:_3="http://xmlns.com/foaf/0.1/"
    xmlns:_4="http://edrn.nci.nih.gov/rdf/schema.rdf#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/pi">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Amber</_3:givenname>
        <_3:surname>Starseraph</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/copi">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Grail</_3:givenname>
        <_3:surname>Wanderer</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/coi">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Jackal</_3:givenname>
        <_3:surname>Magicsoul</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/investigator">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Quake</_3:givenname>
        <_3:surname>Flora</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/peons/1">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Tsunami</_3:givenname>
        <_3:surname>Ravenwitch</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/peons/2">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Cloud</_3:givenname>
        <_3:surname>Steeldevil</_3:surname>
    </rdf:Description>
    <rdf:Description rdf:about="http://html.com/markup/5d/personnel/peons/3">
        <_4:site rdf:resource="http://html.com/markup/5d"/>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
        <_3:givenname>Sephiroth</_3:givenname>
        <_3:surname>Graveguard</_3:surname>
    </rdf:Description>
</rdf:RDF>'''

_manySitesRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about='http://many.com/sites/alpha'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>alpha</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/bravo'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>bravo</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/delta'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>delta</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/charlie'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>charlie</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/echo'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>echo</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/foxtrot'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>foxtrot</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/golf'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>golf</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/hotel'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>hotel</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/india'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/coi"/>
        <_4:title>india</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/juliet'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>juliet</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/kilo'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>kilo</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/lima'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>lima</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/mike'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>mike</_4:title>
        <_3:memberType>Biomarker Developmental Laboratories</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/november'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/coi"/>
        <_4:title>november</_4:title>
        <_3:memberType>Silly</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/oscar'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>oscar</_4:title>
        <_3:memberType>Silly</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/papa'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>papa</_4:title>
        <_3:memberType>Silly</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/quebec'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>quebec</_4:title>
        <_3:memberType>Silly</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/romeo'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>romeo</_4:title>
        <_3:memberType>Foolish</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/sierra'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>sierra</_4:title>
        <_3:memberType>Foolish</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/tango'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>tango</_4:title>
        <_3:memberType>Foolish</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/uniform'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/coi"/>
        <_4:title>uniform</_4:title>
        <_3:memberType>Foolish</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/victor'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>victor</_4:title>
        <_3:memberType>Rash</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/whiskey'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/pi"/>
        <_4:title>whiskey</_4:title>
        <_3:memberType>Rash</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/x'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>x-ray</_4:title>
        <_3:memberType>Rash</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/yankee'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/coi"/>
        <_4:title>yankee</_4:title>
    </rdf:Description>
    <rdf:Description rdf:about='http://many.com/sites/zulu'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_3:pi rdf:resource="http://html.com/markup/5d/personnel/copi"/>
        <_4:title>zulu</_4:title>
        <_3:memberType>Stupendous</_3:memberType>
    </rdf:Description>
</rdf:RDF>'''

_mangledSitesRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:_3="http://edrn.nci.nih.gov/rdf/schema.rdf#" xmlns:_4="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about='http://mangled.com/sites/mangled/b1'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Associate Member B1 - EDRN Funded</_4:title>
        <_3:memberType>Associate Member B1 - EDRN Funded</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://mangled.com/sites/mangled/b2'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Associate Member B2 - Protocol/Project Funded</_4:title>
        <_3:memberType>Associate Member B2 - Protocol/Project Funded</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://mangled.com/sites/mangled/c1'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Associate Member C1 - Non Funded Applicant</_4:title>
        <_3:memberType>Associate Member C1 - Non Funded Applicant</_3:memberType>
    </rdf:Description>
    <rdf:Description rdf:about='http://mangled.com/sites/mangled/c2'>
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
        <_4:title>Assocaite Member C2 - Non Funded Former PI</_4:title>
        <_3:memberType>Assocaite Member C2 - Non Funded Former PI</_3:memberType>
    </rdf:Description>
</rdf:RDF>'''

_emptyPeopleRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>'''

_chileanSiteRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:ns1="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:ns2="http://purl.org/dc/terms/">
  <rdf:Description rdf:about="http://edrn.nci.nih.gov/data/sites/763">
    <ns2:title>Clínica Las Condes/Universidad de chilen</ns2:title>
    <ns1:abbrevName>Wït</ns1:abbrevName>
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Site"/>
    <ns1:staff rdf:resource="http://edrn.nci.nih.gov/data/registered-person/3417"/>
    <ns1:pi rdf:resource="http://edrn.nci.nih.gov/data/registered-person/3417"/>
    <ns1:memberType>Non-EDRN Site</ns1:memberType>
    <ns1:program>🍺</ns1:program>
    <ns1:fwa>♥</ns1:fwa>
    <ns1:historicalNotes>👳</ns1:historicalNotes>
    </rdf:Description>
</rdf:RDF>'''

_chileanPersonRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:ns1="http://edrn.nci.nih.gov/rdf/schema.rdf#"
   xmlns:ns2="http://www.w3.org/2001/vcard-rdf/3.0#"
   xmlns:ns3="http://xmlns.com/foaf/0.1/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="http://edrn.nci.nih.gov/data/registered-person/3417">
    <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Person"/>
    <ns3:givenname>José</ns3:givenname>
    <ns1:middleName></ns1:middleName>
    <ns3:surname>🐰</ns3:surname>
    <ns3:phone>6770🐬128</ns3:phone>
    <ns2:fax>🐤</ns2:fax>
    <ns1:edrnTitle>🎅</ns1:edrnTitle>
    <ns1:specialty>🚲</ns1:specialty>
    <ns1:addr2>Lo Fontecilla 441</ns1:addr2>
    <ns1:country>Chile</ns1:country>
    <ns1:middleName>C</ns1:middleName>
    <ns1:site rdf:resource="http://edrn.nci.nih.gov/data/sites/763"/>
    <ns1:state>Santiago Metropolitan Region&lt;/Mailing_State&gt;&lt;Mailing_Zip&gt;6770128&lt;/Mailing_Zip&gt;&lt;Mailing_State&gt;Santiago Metropolitan Region</ns1:state>
    <ns1:city>Santiago</ns1:city>
    <ns1:addr1>Clínica Las Condes/Universidad de Chile</ns1:addr1>
    <ns3:mbox rdf:resource="mailto:jclavero@clc.cl"/>
  </rdf:Description>
</rdf:RDF>'''

_fakeImage = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

def registerLocalTestData():
    ekeKnowledgeBase.registerTestData('/sites/a', _singleSiteRDF)
    ekeKnowledgeBase.registerTestData('/sites/b', _doubleSiteRDF)
    ekeKnowledgeBase.registerTestData('/sites/c', _duplicateSiteRDF)
    ekeKnowledgeBase.registerTestData('/sites/d', _markedUpSiteRDF)
    ekeKnowledgeBase.registerTestData('/sites/many', _manySitesRDF)
    ekeKnowledgeBase.registerTestData('/people/a', _singlePersonRDF)
    ekeKnowledgeBase.registerTestData('/people/b', _doublePersonRDF)
    ekeKnowledgeBase.registerTestData('/people/aformer', _singleFormerPersonRDF)
    ekeKnowledgeBase.registerTestData('/people/bformer', _doubleFormerPersonRDF)
    ekeKnowledgeBase.registerTestData('/people/moved', _movedPersonRDF)
    ekeKnowledgeBase.registerTestData('/people/many', _manyPeopleRDF)
    ekeKnowledgeBase.registerTestData('/sites/sample', _sampleSiteRDF)
    ekeKnowledgeBase.registerTestData('/people/sample', _samplePersonRDF)
    ekeKnowledgeBase.registerTestData('/people/the-strangler.png', _fakeImage)
    ekeKnowledgeBase.registerTestData('/sites/mangled', _mangledSitesRDF)
    ekeKnowledgeBase.registerTestData('/people/empty', _emptyPeopleRDF)
    ekeKnowledgeBase.registerTestData('/chile/sites', _chileanSiteRDF)
    ekeKnowledgeBase.registerTestData('/chile/people', _chileanPersonRDF)


