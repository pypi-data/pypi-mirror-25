from datetime import timedelta
from freezegun import freeze_time
from ftw.builder import Builder
from ftw.builder import create
from ftw.contentstats.logger import log_stats_to_file
from ftw.contentstats.testing import PatchedLogTZ
from ftw.contentstats.tests import FunctionalTestCase
from operator import itemgetter


class TestLogging(FunctionalTestCase):

    def create_content(self):
        self.set_workflow_chain('Document', 'simple_publication_workflow')
        self.set_workflow_chain('Folder', 'simple_publication_workflow')
        create(Builder('folder'))
        create(Builder('page'))
        create(Builder('page')
               .in_state('published'))

    def test_logs_raw_stats(self):
        self.grant('Contributor')
        self.create_content()
        self.grant('Anonymous')

        log_stats_to_file()
        log_entry = self.get_log_entries()[-1]

        self.assertItemsEqual(
            [u'site', u'timestamp', u'portal_types', u'review_states'],
            log_entry.keys())

        self.assertEquals(
            {u'Folder': 1, u'Document': 2},
            log_entry['portal_types'])

        self.assertEquals(
            {u'private': 2, u'published': 1},
            log_entry['review_states'])

    def test_log_multiple_entries(self):
        # Frozen time is specified in UTC
        # tz_offset specifies what offset to UTC the local tz is supposed to
        # have. This is relevant for stdlib functions that return local times,
        # but *not* for ftw.contentstats, since we never fetch local times
        with freeze_time("2017-07-29 10:30:58.000750", tz_offset=7) as clock:
            with PatchedLogTZ('Europe/Zurich'):
                log_stats_to_file()
                clock.tick(timedelta(days=1))
                log_stats_to_file()

        log_entries = self.get_log_entries()

        self.assertEquals(2, len(log_entries))
        self.assertEquals(
            [u'2017-07-29T12:30:58.000750+02:00',
             u'2017-07-30T12:30:58.000750+02:00'],
            map(itemgetter('timestamp'), log_entries))

    def test_logs_plone_site_id(self):
        log_stats_to_file()
        log_entry = self.get_log_entries()[0]

        self.assertEquals(u'plone', log_entry['site'])

    def test_dst_rollover(self):
        # Start in winter (no DST), half an hour before switch to DST, which
        # will happen at 2017-03-26 01:00:00 UTC / 2017-03-26 02:00:00 CET
        # for Europe/Zurich
        with freeze_time("2017-03-26 00:30:00.000750", tz_offset=7) as clock, \
                PatchedLogTZ('Europe/Zurich'):
            log_stats_to_file()

            # No DST (winter) - UTC offset for Europe/Zurich should be +01:00
            log_entry = self.get_log_entries()[-1]
            self.assertEqual(u'2017-03-26T01:30:00.000750+01:00',
                             log_entry['timestamp'])

            # Forward one hour - rollover from winter to summer, it's now DST
            clock.tick(timedelta(hours=1))
            log_stats_to_file()

            # DST (summer) - UTC offset for Europe/Zurich should be +02:00,
            # and we "magically" skipped the hourd from 02:00 - 03:00
            log_entry = self.get_log_entries()[-1]
            self.assertEqual(u'2017-03-26T03:30:00.000750+02:00',
                             log_entry['timestamp'])

            # Fast forward to October, half an hour before end of DST
            clock.move_to("2017-10-29 00:30:00.000750")
            log_stats_to_file()

            # We're still just in DST (summer) - UTC offset for
            # Europe/Zurich should be +02:00
            log_entry = self.get_log_entries()[-1]
            self.assertEqual(u'2017-10-29T02:30:00.000750+02:00',
                             log_entry['timestamp'])

            # Forward one hour - rollover from summer to winter, DST ends
            clock.tick(timedelta(hours=1))
            log_stats_to_file()

            # No DST (winter) - UTC offset for Europe/Zurich should be +01:00,
            # and it's now "magically" 02:30 again, even though an hour passed
            log_entry = self.get_log_entries()[-1]
            self.assertEqual(u'2017-10-29T02:30:00.000750+01:00',
                             log_entry['timestamp'])
