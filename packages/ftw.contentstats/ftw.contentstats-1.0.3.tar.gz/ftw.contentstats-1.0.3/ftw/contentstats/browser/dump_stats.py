from ftw.contentstats.logger import log_stats_to_file
from zExceptions import Unauthorized
from zope.publisher.browser import BrowserView


class DumpContentStatsView(BrowserView):
    """Dumps content statistics to a logfile.

    This view is accessible to Anonymous (zope.Public), but *only* when
    requested from localhost!

    This is so it can easily be triggered from cron jobs or scripts running
    on the same host as the Plone site, without the need to store credentials.
    """

    def _verify_access(self):
        # Only allow access from localhost
        src_ip = self.request.getClientAddr()
        if src_ip != '127.0.0.1':
            raise Unauthorized()

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'text/plain')
        self._verify_access()

        if self.request.method.upper() != 'POST':
            self.request.response.setStatus(405)
            return 'Method not allowed, please POST'

        log_stats_to_file()
        self.request.response.setStatus(204)
        return ''
