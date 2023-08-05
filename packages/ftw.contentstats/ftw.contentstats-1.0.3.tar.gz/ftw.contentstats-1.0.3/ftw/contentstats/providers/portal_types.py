from ftw.contentstats.interfaces import IStatsKeyFilter
from ftw.contentstats.interfaces import IStatsProvider
from plone import api
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface


@implementer(IStatsProvider)
@adapter(IPloneSiteRoot, Interface)
class PortalTypesProvider(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def title(self):
        """Human readable title
        """
        return u'Portal type statistics'

    def _get_filter(self):
        return queryMultiAdapter((self.context, self.request),
                                 IStatsKeyFilter, name='portal_types')

    def get_raw_stats(self):
        """Return a list of dicts (keys: name, amount).
        """
        counts = {}
        key_filter = self._get_filter()
        catalog = api.portal.get_tool('portal_catalog')
        index = catalog._catalog.indexes['portal_type']
        for key in index.uniqueValues():
            if key_filter and not key_filter.keep(key):
                continue
            t = index._index.get(key)
            if not isinstance(t, int):
                counts[key] = len(t)
            else:
                counts[key] = 1
        return counts

    def get_display_names(self):
        """Return a id, title mapping of all portal types as display names.
        """
        portal_types = api.portal.get_tool('portal_types')
        ftis = portal_types.values()
        titles = [
            (fti.id, translate(
                fti.title, domain=fti.i18n_domain, context=self.request))
            for fti in ftis]
        return dict(titles)
