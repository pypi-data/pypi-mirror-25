from ftw.contentstats.interfaces import IStatsKeyFilter
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IStatsKeyFilter)
@adapter(IPloneSiteRoot, Interface)
class PortalTypesFilter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def keep(self, key):
        whitelist = ['Document', 'Event']
        if key in whitelist:
            return True
        return False


@implementer(IStatsKeyFilter)
@adapter(IPloneSiteRoot, Interface)
class ReviewStatesFilter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def keep(self, key):
        whitelist = ['published']
        if key in whitelist:
            return True
        return False
