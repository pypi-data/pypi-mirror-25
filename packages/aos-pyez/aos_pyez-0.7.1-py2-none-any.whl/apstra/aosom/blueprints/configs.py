# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

from apstra.aosom.blueprints.widget import BlueprintWidget
from apstra.aosom.exc import SessionRqstError

__all__ = ['BlueprintConfigs']


class BlueprintConfigs(BlueprintWidget):

    def get_url(self, node_id):
        return self.url + "/nodes/" + node_id + '/config-rendering'

    def get(self, label=None, node_id=None):
        if label:
            node_id = self.blueprint.graph.node_ids['system_nodes'].from_label(label)

        if not node_id:
            raise ValueError("missing node_id value")

        got = self.api.requests.get(self.get_url(node_id=node_id))
        if not got.ok:
            raise SessionRqstError(
                resp=got,
                message="unable to get config: {}".format(got.text))

        return got.json()['config']

    def __getitem__(self, label):
        return self.get(label=label)
