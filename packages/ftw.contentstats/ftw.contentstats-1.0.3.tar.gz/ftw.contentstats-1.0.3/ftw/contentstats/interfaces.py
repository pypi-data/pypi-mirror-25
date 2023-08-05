from zope.interface import Interface


class IStatsProvider(Interface):
    """Interface for stats provider adapters
    """

    def __init__(context, request):
        """Adapts context and request, context is usually a Plone site"""

    def title():
        """Return a human readable title of the stats provider
        """

    def get_raw_stats():
        """Extract and return raw stats.

        Return value is a dict with key:value pairs, where key should be a
        stable, internal ID. If a different display name is desired, a mapping
        should be provided by implementing get_display_names().
        """

    def get_display_names():
        """Return a key: display_name mapping of human readable key names.

        If no alternate display names are needed, this should return None.
        """


class IStatsKeyFilter(Interface):
    """Interface for named adapters that allow stats providers to filter their
    returned stats data by key.

    The adapter name indicates what type of keys it's supposed to be applied
    to by stats providers, e.g. 'portal_types', 'review_states', ...
    """

    def __init__(context, request):
        """Adapts context and request, context is usually a Plone site"""

    def keep(key):
        """Returns ``True`` if the key in question should be kept, ``False``
        otherwise.
        """
