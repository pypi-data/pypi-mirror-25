from ftw.builder import Builder
from ftw.builder import create
from ftw.contentstats.testing import CONTENTSTATS_FUNCTIONAL_ZSERVER
from ftw.contentstats.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from requests_toolbelt.adapters.source import SourceAddressAdapter
import sys
import unittest


class TestContentStatsView(FunctionalTestCase):

    layer = CONTENTSTATS_FUNCTIONAL_ZSERVER

    def setUp(self):
        super(TestContentStatsView, self).setUp()
        self.grant('Anonymous')

    def create_content(self):
        self.set_workflow_chain('Document', 'simple_publication_workflow')
        self.set_workflow_chain('Folder', 'simple_publication_workflow')
        create(Builder('folder'))
        create(Builder('page'))
        create(Builder('page')
               .in_state('published'))

    @browsing
    def test_causes_stats_to_be_logged(self, browser):
        self.grant('Contributor')
        self.create_content()
        self.grant('Anonymous')

        browser.open(self.portal, view='@@dump-content-stats', method='POST')
        log_entry = self.get_log_entries()[-1]

        self.assertEquals(
            [u'review_states', u'portal_types', u'site', u'timestamp'],
            log_entry.keys())

        self.assertEquals(
            {u'Folder': 1, u'Document': 2},
            log_entry['portal_types'])

    @browsing
    def test_access_from_localhost_allowed_for_anonymous(self, browser):
        browser.open(self.portal, view='@@dump-content-stats', method='POST')
        self.assertEquals(204, browser.status_code)

    # Mac OS rejects source addresses other than 127.0.0.1 from the loopback
    # interface with "[Errno 49] Can't assign requested address"
    @unittest.skipIf(sys.platform == 'darwin', "Can't test this on Mac OS")
    @browsing
    def test_only_allows_access_from_localhost(self, browser):
        source = SourceAddressAdapter('127.0.0.42')
        browser.get_driver().requests_session.mount('http://', source)
        dump_stats_url = (
            'http://localhost:%s/%s/@@dump-content-stats' % (
                self.zserver_port, self.portal.id))

        with browser.expect_unauthorized():
            browser.open(dump_stats_url)

        with browser.expect_unauthorized():
            browser.open(dump_stats_url, method='POST')

    @browsing
    def test_only_accepts_post_method(self, browser):
        with browser.expect_http_error(code=405):
            browser.open(self.portal, view='@@dump-content-stats')

        browser.open(self.portal, view='@@dump-content-stats', method='POST')
        self.assertEquals(204, browser.status_code)
