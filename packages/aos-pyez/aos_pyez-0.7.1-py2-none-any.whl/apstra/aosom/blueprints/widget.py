# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula


class BlueprintWidget(object):
    def __init__(self, owner):
        self.blueprint = owner
        self.api = self.blueprint.api
        self.url = self.blueprint.url
