# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_base
from eke.knowledge.testing import EKE_KNOWLEDGE_FIXTURE
from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from plone.testing import z2
from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager

_sentMessages = []

class _TestingMailHost(object):
    smtp_queue = True
    def __init__(self):
        self.resetSentMessages()
    def send(self, message, mto=None, mfrom=None, subject=None, encode=None, immediate=False, charset=None, msg_type=None):
        global _sentMessages
        _sentMessages.append(message)
    def resetSentMessages(self):
        global _sentMessages
        _sentMessages = []
    def getSentMessages(self):
        global _sentMessages
        return _sentMessages
    def getId(self):
        return 'MailHost'

_testingMailHost = _TestingMailHost()

class EKESite(PloneSandboxLayer):
    defaultBases = (EKE_KNOWLEDGE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import eke.site
        self.loadZCML(package=eke.site)
        z2.installProduct(app, 'eke.site')
        import eke.site.tests.base
        eke.site.tests.base.registerLocalTestData()
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'eke.site:default')
        portal._original_MailHost = portal.MailHost
        portal.MailHost = _testingMailHost
        siteManager = getSiteManager(portal)
        siteManager.unregisterUtility(provided=IMailHost)
        siteManager.registerUtility(_testingMailHost, provided=IMailHost)
        portal._setPropValue('email_from_address', u'edrn-ic@jpl.nasa.gov')
        portal._setPropValue('email_from_name', u'EDRN Informatics Center')
    def teatDownPloneSite(self, portal):
        portal.MailHost = portal._original_MailHost
        siteManager = getSiteManager(portal)
        siteManager.unregisterUtility(provided=IMailHost)
        siteManager.registerUtility(aq_base(portal._original_MailHost), IMailHost)
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'eke.site')

EKE_SITE_FIXTURE = EKESite()
EKE_SITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EKE_SITE_FIXTURE,),
    name='EKESite:Integration',
)
EKE_SITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EKE_SITE_FIXTURE,),
    name='EKESite:Functional',
)
