from ftw.contentstats.testing import CONTENTSTATS_FUNCTIONAL
from ftw.contentstats.testing import get_log_path
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import json
import os
import transaction


class FunctionalTestCase(TestCase):
    layer = CONTENTSTATS_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.load_zcml_string = self.layer['load_zcml_string']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()

    def set_workflow_chain(self, for_type, to_workflow):
        wftool = api.portal.get_tool('portal_workflow')
        wftool.setChainForPortalTypes((for_type,),
                                      (to_workflow,))

    def get_log_entries(self):
        log_path = get_log_path()
        with open(log_path) as log:
            entries = map(json.loads, log.readlines())
        return entries

    @property
    def zserver_port(self):
        return str(os.environ.get('ZSERVER_PORT', 55001))
