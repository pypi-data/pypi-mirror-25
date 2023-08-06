# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

import retrying
from collections import defaultdict

from apstra.aosom.exc import SessionRqstError
from apstra.aosom.utils.collection import CollectionItem
from apstra.aosom.utils.dynmodldr import DynamicModuleOwner
from .registry import register_architecture


class BlueprintCollectionItem(CollectionItem, DynamicModuleOwner):
    """
    This class provides :class:`Blueprint` item instance management.
    """
    ReferenceArchitecture = None           # default blueprint item class

    DynamicModuleConf = [{
        'package': __package__,
        'modules': {
            'graph': "graph",
            'configs': "configs",
        }
    }]

    # =========================================================================
    #
    #                             PROPERTIES
    #
    # =========================================================================

    @property
    def version(self):
        got = self.graph.query(contents="{ version }")
        return got['data']['version']

    @property
    def reference_arch(self):
        return self.value.get('design')

    # -------------------------------------------------------------------------
    # PROPERTY: contents
    # -------------------------------------------------------------------------

    @property
    def contents(self):
        """
        Property accessor to blueprint contents.

        Raises:
            SessionRqstError: upon issue with HTTP requests
        """
        got = self.api.requests.get(self.url)
        if not got.ok:
            raise SessionRqstError(
                message='unable to get blueprint contents',
                resp=got)

        return got.json()

    # -------------------------------------------------------------------------
    # PROPERTY: build_errors
    # -------------------------------------------------------------------------

    @property
    def build_errors(self):
        """
        Property accessor to any existing blueprint build errors.

        Raises:
            SessionReqstError: upon error with obtaining the blueprint contents

        Returns:
            - <list> of existing errors, could be empty list if no errors
        """
        got = self.graph.query(contents="{errors}")
        return got['data']['errors']

    @property
    def anomalies(self):
        return self.api.requests.get(self.url + "/anomalies").json()

    @property
    def anomalies_by_type(self):
        at_data = defaultdict(list)
        for item in self.anomalies['items']:
            at_data[item['anomaly_type']].append(item)
        return dict(at_data)

    @property
    def anomalies_by_system(self):
        at_data = defaultdict(list)
        for item in self.anomalies['items']:
            at_data[item['identity']['system_id']].append(item)
        return dict(at_data)

    # =========================================================================
    #
    #                             PUBLIC METHODS
    #
    # =========================================================================

    def create(self, value=None, replace=False, **kwargs):

        assert value
        if 'label' not in value:
            value['label'] = self.name

        super(BlueprintCollectionItem, self).create(value)

        if 'no_wait' in value:
            return True

        blocking_wait = value.get('blocking_wait', 10000)

        @retrying.retry(wait_fixed=1000, stop_max_delay=blocking_wait)
        def wait_for_blueprint():
            assert self.version > 0

        # noinspection PyBroadException
        try:
            wait_for_blueprint()
        except:
            return False

        return True

    # def create(self, template_id, reference_arch, blocking_wait=10000):
    #     data = dict(
    #         label=self.name,
    #         design=reference_arch,
    #         template_id=template_id,
    #         init_type='template_reference')
    #
    #     super(BlueprintCollectionItem, self).create(data)
    #
    #     if not blocking_wait:
    #         return True
    #
    #     @retrying.retry(wait_fixed=1000, stop_max_delay=blocking_wait)
    #     def wait_for_blueprint():
    #         assert self.version > 0
    #
    #     # noinspection PyBroadException
    #     try:
    #         wait_for_blueprint()
    #     except:
    #         return False
    #
    #     return True

    def await_build_ready(self, timeout=5000):
        """
        Wait a specific amount of `timeout` for the blueprint build status
        to return no errors.  The waiting polling interval is fixed at 1sec.

        Args:
            timeout (int): timeout to wait in milliseconds

        Returns:
            True: when the blueprint contains to build errors
            False: when the blueprint contains build errors, even after waiting `timeout`

        """
        @retrying.retry(wait_fixed=1000, stop_max_delay=timeout)
        def wait_for_no_errors():
            assert not self.build_errors

        # noinspection PyBroadException
        try:
            wait_for_no_errors()
        except:
            return False

        return True

    def deploy(self, version=None):
        api = self.api.requests
        version = version or self.version
        return api.put(self.url + "/deploy", json=dict(version=version))

    @classmethod
    def register_arch(cls, arch_name=None):
        register_architecture(arch_name or cls.ReferenceArchitecture, cls)


BlueprintCollectionItem.register_arch()
