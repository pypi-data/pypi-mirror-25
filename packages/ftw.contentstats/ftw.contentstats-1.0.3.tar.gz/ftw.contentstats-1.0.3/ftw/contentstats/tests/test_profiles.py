from ftw.contentstats.tests import FunctionalTestCase
from plone import api


PROFILE = 'ftw.contentstats:default'


class TestDefaultProfile(FunctionalTestCase):

    def test_installed(self):
        portal_setup = api.portal.get_tool('portal_setup')
        version = portal_setup.getLastVersionForProfile(PROFILE)
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')
