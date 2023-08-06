import json
from bidict import bidict

from apstra.aosom.exc import SessionRqstError


class NodeTypeCache(bidict):
    GraphQL_query = dict(
        get_node_by_type_id="""
    {
       node: %s(id: "%s") {
          id
          label
       }
    }
    """,

    get_node_by_type_label="""
    {
       node: %s(label: "%s") {
          id
          label
       }
    }
    """,

    get_node_catalog="""
    {
        nodes: %s {
            id
            label
        }
    }
    """)

    @property
    def labels(self):
        return self.inv

    def __init__(self, node_type, graph):
        super(NodeTypeCache, self).__init__()
        self.node_type = node_type
        self.graph = graph

    def add_by_id(self, node_id):
        query = self.GraphQL_query['get_node_by_type_id'] % (self.node_type, node_id)
        got = self.graph.query(contents=query)

        try:
            node = got['data']['node'][0]
        except IndexError:
            raise ValueError("node_id '%s' not found" % node_id)

        self.put(key=node['id'], val=node['label'])

    def add_by_label(self, node_label):
        query = self.GraphQL_query['get_node_by_type_label'] % (self.node_type, node_label)
        got = self.graph.query(contents=query)

        try:
            node = got['data']['node'][0]
        except IndexError:
            raise ValueError("node_label '%s' not found" % node_label)

        self.put(key=node['id'], val=node['label'])

    def catalog(self):
        query = self.GraphQL_query['get_node_catalog'] % self.node_type
        got = self.graph.query(contents=query)
        for node in got['data']['nodes']:
            self.put(key=node['id'], val=node['label'])

    def to_label(self, node_id):
        if node_id not in self:
            self.add_by_id(node_id)
        return self.get(node_id)

    def from_label(self, node_label):
        if node_label not in self.inv:
            self.add_by_label(node_label)
        return self.inv.get(node_label)


class NodeRegistryCache(object):
    def __init__(self, graph):
        self.graph = graph
        self._of_type = dict()

    def __getitem__(self, node_type):
        if node_type not in self._of_type:
            self._of_type[node_type] = NodeTypeCache(
                node_type=node_type, graph=self.graph)

        return self._of_type[node_type]


class BlueprintGraphNode(object):
    def __init__(self, graph, node_id, read=True):
        self.graph = graph
        self.blueprint = graph.blueprint
        self.api = self.blueprint.api
        self.url = self.blueprint.url + "/nodes/" + node_id
        self.id = node_id
        self.value = None

        if read is True:
            self.read()

    def read(self):
        got = self.api.requests.get(self.url)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)
        self.value = got.json()

    def write(self, value=None):
        got = self.api.requests.patch(self.url, json=value or self.value)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)

        self.read()

    def __str__(self):
        return json.dumps(self.value, indent=3)

    __repr__ = __str__
