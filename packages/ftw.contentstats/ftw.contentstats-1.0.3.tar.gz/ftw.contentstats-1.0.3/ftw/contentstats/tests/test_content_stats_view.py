from ftw.builder import Builder
from ftw.builder import create
from ftw.contentstats.stats import ContentStats
from ftw.contentstats.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from zExceptions import Unauthorized


class TestContentStatsView(FunctionalTestCase):

    def setUp(self):
        super(TestContentStatsView, self).setUp()
        self.grant('Manager')

    def create_content(self):
        self.set_workflow_chain('Document', 'simple_publication_workflow')
        self.set_workflow_chain('Folder', 'simple_publication_workflow')
        create(Builder('folder'))
        create(Builder('page'))
        create(Builder('page')
               .in_state('published'))

    def test_content_stats_view_only_accessible_for_manager(self):
        self.grant('Contributor', 'Editor', 'Reviewer', 'Publisher')
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@content-stats')

    @browsing
    def test_view_lists_type_counts_in_table(self, browser):
        self.create_content()
        browser.login().open(self.portal, view='@@content-stats')
        table = browser.css('#content-stats-portal_types').first
        self.assertEqual(
            [['', 'Folder', '1'], ['', 'Page', '2']],
            table.lists())

    @browsing
    def test_view_lists_review_states_in_table(self, browser):
        self.create_content()
        browser.login().open(self.portal, view='@@content-stats')
        table = browser.css('#content-stats-review_states').first
        self.assertEqual(
            [['', 'private', '2'], ['', 'published', '1']],
            table.lists())

    @browsing
    def test_editable_border_disabled(self, browser):
        browser.login().open(self.portal, view='@@content-stats')
        self.assertEqual(0, len(browser.css('#content-views')))

    @browsing
    def test_data_attribute_with_data_url(self, browser):
        browser.login().open(self.portal, view='@@content-stats')
        self.assertEqual(
            'http://nohost/plone/content-stats-json?stat=portal_types',
            browser.css('#content-stats-data-portal_types').first.attrib[
                'data-stat-data-url'])

    @browsing
    def test_json_endpoint_returns_404_for_missing_stat(self, browser):
        self.create_content()
        browser.login()

        with browser.expect_http_error(code=404):
            browser.open(self.portal, view='content-stats-json')

        self.assertEquals('application/json',
                          browser.headers.get('Content-Type'))

        self.assertDictEqual({}, browser.json)

    @browsing
    def test_json_endpoint_stats_by_name(self, browser):
        self.create_content()
        browser.login()

        browser.open(self.portal, view='content-stats-json?stat=portal_types')

        self.assertEquals('application/json',
                          browser.headers.get('Content-Type'))

        self.assertDictEqual(
            ContentStats().get_human_readable_stats()['portal_types']['data'],
            browser.json)
