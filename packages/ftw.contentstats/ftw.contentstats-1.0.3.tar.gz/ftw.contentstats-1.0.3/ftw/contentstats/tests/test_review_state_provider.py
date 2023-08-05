from ftw.builder import Builder
from ftw.builder import create
from ftw.contentstats.interfaces import IStatsProvider
from ftw.contentstats.tests import FunctionalTestCase
from zope.component import getMultiAdapter


class TestReviewStatesProvider(FunctionalTestCase):

    def setUp(self):
        super(TestReviewStatesProvider, self).setUp()
        self.grant('Manager')

        self.provider = getMultiAdapter((self.portal, self.portal.REQUEST),
                                        IStatsProvider,
                                        name='review_states')

    def create_content(self):
        self.set_workflow_chain('Document', 'simple_publication_workflow')
        self.set_workflow_chain('Folder', 'simple_publication_workflow')
        create(Builder('folder'))
        create(Builder('page'))
        create(Builder('page')
               .in_state('published'))

    def test_review_states_counts_empty(self):
        counts = self.provider.get_raw_stats()
        self.assertEqual({}, counts)

    def test_review_states_counts_reported_correctly(self):
        self.create_content()
        counts = self.provider.get_raw_stats()
        self.assertEqual({'private': 2, 'published': 1}, counts)

    def test_display_names_reported_correctly(self):
        self.create_content()
        titles = self.provider.get_display_names()
        self.assertDictContainsSubset({
            'private': u'private',
            'published': u'published'},
            titles)

    def test_respects_review_states_filter(self):
        self.create_content()
        self.load_zcml_string('<include package="ftw.contentstats.demo" />')
        counts = self.provider.get_raw_stats()
        self.assertEqual({'published': 1}, counts)
