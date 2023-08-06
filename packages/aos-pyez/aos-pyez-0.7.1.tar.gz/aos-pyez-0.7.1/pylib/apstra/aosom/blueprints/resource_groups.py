# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

from apstra.aosom.exc import NoExistsError
from apstra.aosom.utils.collection import Collection
from apstra.aosom.utils.collection_item import CollectionItem

__all__ = ['ResourceGroups']


class ResourceGroupItem(CollectionItem):
    PoolTypeResourceManagers = {
        'ip': 'IpPools',
        'asn': 'AsnPools'
    }

    @property
    def resource_type(self):
        return self.value['type']

    @property
    def url(self):
        """
        Property accessor for item URL.

        :getter: returns the URL string for this specific item
        """

        if not self.exists:
            raise NoExistsError("name=%s, collection=%s" %
                                (self.name, self.collection.url))

        return "%s/%s/%s" % (self.collection.url,
                             self.resource_type,
                             self.id)

    @property
    def pool_ids(self):
        return self.value['pool_ids']

    @property
    def pool_names(self):
        # get the aos session resource manager for this resource type

        _rm = getattr(self.api.session,
                      self.PoolTypeResourceManagers[self.resource_type])

        # now map the ID values to LABEL values for each pool-id
        # and return that list

        _by = "by_%s" % _rm.UNIQUE_ID
        return [_rm.cache[_by][p_id][_rm.LABEL] for p_id in self.pool_ids]

    @pool_ids.setter
    def pool_ids(self, pool_list):
        if not isinstance(pool_list, list):
            raise ValueError("pool_list must be <list>")

        self.write(value=dict(pool_ids=pool_list))
        self.collection._update_cache(self)

    def delete(self):
        """
        This will simply write an empty list value into the resource pool_list
        """
        self.pool_ids = []
        self.collection._update_cache(self)

    def create(self, value=None, replace=False):
        raise RuntimeError("create not support on resource item")


class ResourceGroups(Collection):
    Item = ResourceGroupItem
    LABEL = 'name'
    UNIQUE_ID = 'name'
    URI = 'resource_groups'

    def _update_cache(self, item):
        self._cache['by_%s' % self.LABEL][item.name].update(item.value)
        self._cache['by_%s' % self.UNIQUE_ID][item.id].update(item.value)
