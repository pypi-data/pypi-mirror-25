# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula

import json

from graphql.utils.introspection_query import introspection_query

from apstra.aosom.exc import SessionRqstError

from .widget import BlueprintWidget
from .graph_node import BlueprintGraphNode
from .graph_node import NodeRegistryCache
from .graph_relationship import BlueprintGraphRelationship


__all__ = ['BlueprintGraph']


class BlueprintGraph(BlueprintWidget):
    _GQL_ = dict(
        query_catalog="""{
          query: __type(name: "Query") {
            fields {
              name
              type {
                kind
                name
                ofType {
                  name
                }
              }
              args {
                name
              }
            }
          }
        }
        """,
        node_type="""
            query Query {
              node: __type(name: "%s") {
                ... FullType
              }
            }

            fragment FullType on __Type {
                kind
                name
                fields {
                  name
                  type {
                    ...TypeRef
                  }
                }
            }

            fragment TypeRef on __Type {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
            }
        """)

    def __init__(self, owner):
        super(BlueprintGraph, self).__init__(owner=owner)
        self.url = self.blueprint.url + "/ql"
        self.query_catalog = dict()
        self.node_type_catalog = dict()
        self.node_ids = NodeRegistryCache(self)
        self.build_catalog()

    def get_schema(self, fileobj=None, indent=3):
        got = self.query(contents=introspection_query)
        if fileobj is not None:
            json.dump(got, fileobj, indent=indent)
        else:
            return got

    def build_catalog(self):
        got = self.query(contents=self._GQL_['query_catalog'])
        fields = got['data']['query']['fields']

        def humanize_type(i_type):
            if i_type['kind'] != 'LIST':
                return i_type['name']
            else:
                return {
                    'type': i_type['ofType']['kind'],
                    'kind': i_type['ofType']['name'] or i_type['ofType']['ofType']
                }

        for each in fields:
            ent = {
                'args': [a['name'] for a in each['args']]
            }

            kind = each['type']['kind']
            ent['type'] = kind
            if kind == 'LIST':
                ent['LIST'] = each['type']['ofType']['name']
            elif kind == 'SCALAR':
                ent['SCALAR'] = each['type']['name']

            self.query_catalog[each['name']] = ent

        def build_node_ent(_of_type):
            node_info = self.query(contents=self._GQL_['node_type'] % _of_type)['data']['node']
            self.node_type_catalog[_of_type] = {
                field['name']: {
                    'type': field['type']['kind'],
                    field['type']['kind']: humanize_type(field['type'])

                }
                for field in node_info['fields']
            }

        for each in filter(lambda name: name.endswith("_nodes"), self.query_catalog):
            ent = self.query_catalog[each]
            of_type = ent.get('LIST')
            if not of_type:
                continue
            build_node_ent(_of_type=of_type)

    def query(self, contents=None, mode='ql', **kwargs):
        post_data = dict(query=contents)
        support_modes = ['ql', 'qe']
        if mode not in support_modes:
            raise ValueError("mode is not one of support: {}".format(support_modes))

        if not post_data['query']:
            try:
                if 'fileobj' in kwargs:
                    post_data['query'] = kwargs['fileobj'].read()
            except Exception as exc:
                raise RuntimeError("no query text: {}".format(str(exc)))

        if not post_data['query']:
            raise ValueError("missing query text")

        if 'variables' in kwargs:
            post_data['variables'] = json.dumps(kwargs['variables'])

        url = "%s/%s" % (self.blueprint.url, mode)
        got = self.api.requests.post(url, json=post_data)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)

        return got.json()

    def query_ae(self, contents):
        url = self.blueprint.url + "/qe"
        post_data = dict(query=contents)
        got = self.api.requests.post(url, json=post_data)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)
        return got.json()

    def get_node(self, node_id):
        return BlueprintGraphNode(graph=self, node_id=node_id)

    def get_rel(self, rel_id):
        return BlueprintGraphRelationship(graph=self, rel_id=rel_id)
