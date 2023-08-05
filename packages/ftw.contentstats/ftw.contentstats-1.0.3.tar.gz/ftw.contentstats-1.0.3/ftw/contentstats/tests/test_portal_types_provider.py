from ftw.builder import Builder
from ftw.builder import create
from ftw.contentstats.interfaces import IStatsProvider
from ftw.contentstats.tests import FunctionalTestCase
from zope.component import getMultiAdapter


class TestPortalTypesProvider(FunctionalTestCase):

    def setUp(self):
        super(TestPortalTypesProvider, self).setUp()
        self.grant('Manager')

        self.provider = getMultiAdapter((self.portal, self.portal.REQUEST),
                                        IStatsProvider,
                                        name='portal_types')

    def create_content(self):
        create(Builder('folder'))
        create(Builder('page'))
        create(Builder('page'))

    def test_type_counts_empty(self):
        counts = self.provider.get_raw_stats()
        self.assertEqual({}, counts)

    def test_type_counts_reported_correctly(self):
        self.create_content()
        counts = self.provider.get_raw_stats()
        self.assertEqual({u'Folder': 1, u'Document': 2}, counts)

    def test_display_names_reported_correctly(self):
        titles = self.provider.get_display_names()
        self.assertDictContainsSubset({
            'Discussion Item': u'Comment',
            'Document': u'Page',
            'News Item': u'News Item'},
            titles)

    def test_respects_portal_types_filter(self):
        self.create_content()
        self.load_zcml_string('<include package="ftw.contentstats.demo" />')
        counts = self.provider.get_raw_stats()
        self.assertEqual({u'Document': 2}, counts)
