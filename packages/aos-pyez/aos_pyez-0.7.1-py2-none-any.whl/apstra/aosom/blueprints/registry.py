# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula


__all__ = ['register_architecture']


_Registry = dict()


def _registered_architecture(*vargs, **kwargs):
    try:
        ref_arch = kwargs['datum']['design']
    except:
        ref_arch = None
    itemcls = _Registry.get(ref_arch) or _Registry.get(None)
    return itemcls(**kwargs)


def register_architecture(reference_arch, blueprint_cls):
    _Registry[reference_arch] = blueprint_cls
