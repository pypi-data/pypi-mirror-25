# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

from apstra.aosom.utils.collection import Collection
from .registry import _registered_architecture

__all__ = ['Blueprints']


class Blueprints(Collection):
    """
    Blueprints collection class provides management of AOS blueprint instances.
    """
    URI = 'blueprints'
    LABEL = 'label'
    Item = _registered_architecture
