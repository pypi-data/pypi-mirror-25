import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from zope.component import createObject
from ..testing import SPARC_REQUESTS_INTEGRATION_LAYER
from .. import IRequest, IRequestResolver

import sparc.requests.request

class SparcRequestsRequestTestCase(unittest.TestCase):
    layer = SPARC_REQUESTS_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def unregister_request(self):
        self.sm.unregisterUtility(
            component=sparc.requests.request.SparcRequest, 
            provided=IRequest)
    
    def register_request(self):
        self.sm.registerUtility(
            component=sparc.requests.request.SparcRequest, 
            provided=IRequest)

    def test_factory(self):
        self.assertTrue(IRequest.providedBy(createObject(u'sparc.requests.request')))
    
    def test_singleton(self):
        self.assertTrue(IRequest.providedBy(self.sm.getUtility(IRequest)))
    
    def test_request_resolver(self):
        req = createObject(u'sparc.requests.request')
        
        resolver = self.sm.getUtility(IRequestResolver)
        self.assertIs(resolver(request=req), req)
        
        registered_req = self.sm.getUtility(IRequest)
        self.assertIs(resolver(), registered_req)
        
        self.unregister_request()
        self.assertIsNot(resolver(), registered_req)
        
        self.register_request()
        self.assertIs(resolver(), registered_req)
        

class test_suite(test_suite_mixin):
    layer = SPARC_REQUESTS_INTEGRATION_LAYER
    package = 'sparc.requests'
    module = 'request'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcRequestsRequestTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])