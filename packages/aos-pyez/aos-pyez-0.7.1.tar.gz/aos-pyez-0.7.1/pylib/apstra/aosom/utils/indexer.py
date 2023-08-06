# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula


class Indexer(object):
    INDEX = 'label'
    INDEX_OPT = ('id', 'label')

    def __init__(self):
        self._index = 'label'
        self._cache = dict(id={}, label={})

    @property
    def cache(self):
        return self._cache

    @property
    def by(self):
        return self._index

    @by.setter
    def by(self, value):
        if value not in self.INDEX_OPT:
            raise ValueError("value provided not valid")
        self._index = value

    def ingest(self, data_list):
        for each in data_list:
            self._cache['label'][each['label']] = each
            self._cache['id'][each['id']] = each

    def id_to_label(self, value_id):
        return self._cache['id'][value_id]['label']

    def lable_to_id(self, value_label):
        return self._cache['label'][value_label]['id']

    def keys(self):
        return self._cache[self.by].keys()

    def __getitem__(self, value):
        ret_idx = self.INDEX_OPT[(self.INDEX_OPT.index(self.by) + 1) % 2]
        item = self._cache[self.by].get(value)
        return None if not item else item[ret_idx]

    def __contains__(self, value):
        return value in self._cache[self.by]

    def __len__(self):
        return len(self._cache[self.by])
