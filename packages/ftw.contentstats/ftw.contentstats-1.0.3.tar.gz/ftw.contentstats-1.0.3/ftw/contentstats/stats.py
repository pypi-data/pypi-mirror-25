from ftw.contentstats.interfaces import IStatsProvider
from zope.component import getAdapters
from zope.component.hooks import getSite


class ContentStats(object):
    """Gather content statistics from the Plone site.
    """

    def __init__(self):
        """This utility class requires a Plone site.
        """
        if not self.plone:
            raise Exception('Please setup a Plone site')

    @property
    def plone(self):
        """Get Plone site from globals
        """
        return getSite()

    def _get_providers(self):

        return getAdapters((self.plone, self.plone.REQUEST),
                           IStatsProvider)

    def get_provider_names(self):
        """Get names of all registered stats providers.
        """
        return [name for name, adapter_ in self._get_providers()]

    def get_raw_stats(self):
        """Get a dictionary with raw stats from all registered providers.

        This is the main API for accessing the machine readable representation
        of the collected stats.
        """
        stats = {}
        for name, provider in self._get_providers():
            stats[name] = provider.get_raw_stats()
        return stats

    def get_stats_titles(self):
        """Get a name:title mapping for titles of all providers.
        """
        titles = {}
        for name, provider in self._get_providers():
            titles[name] = provider.title()
        return titles

    def get_stats_display_names(self):
        """Get a name:display_names mapping with display_names dicts of
        all providers.

        If a provider returns None for its display_names mapping, this
        method substitutes it with an empty dict for easy processing below.
        """
        display_names = {}
        for name, provider in self._get_providers():
            display_names[name] = {}
            names = provider.get_display_names()
            if names:
                display_names[name] = names
        return display_names

    def get_human_readable_stats(self):
        """Get a dictionary that combines all stats with their metadata.

        This includes stat titles as well as rewriting internal keys to
        display names. This is used in the template and JSON view, where
        a human readable representation is desired.
        """
        raw_stats = self.get_raw_stats()
        titles = self.get_stats_titles()
        display_names = self.get_stats_display_names()

        human_readable_stats = {}
        for stat_name in self.get_provider_names():
            stat_dict = {}
            stat_dict['title'] = titles[stat_name]
            stat_dict['data'] = {}

            # Rewrite internal keys to display names if necessary
            names = display_names.get(stat_name, {})
            for key, value in raw_stats[stat_name].items():
                # Try for a display name, default to key
                display_name = names.get(key, key)
                stat_dict['data'][display_name] = value

            human_readable_stats[stat_name] = stat_dict

        return human_readable_stats
