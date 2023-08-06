import json
from apstra.aosom.exc import SessionRqstError


class BlueprintGraphRelationship(object):
    def __init__(self, graph, rel_id=None, read=True):

        self.graph = graph
        self.blueprint = graph.blueprint
        self.api = self.blueprint.api
        self._baseurl = self.blueprint.url + "/relationships"
        self.id = rel_id
        self.value = None

    @property
    def url(self):
        if not self.id:
            raise RuntimeError("no relationship id")
        return "%s/%s" % (self._baseurl, self.id)

    def delete(self):
        got = self.api.requests.delete(self.url)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)
        self.value = None

    def read(self):
        got = self.api.requests.get(self.url)
        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)
        self.value = got.json()

    def create(self, source_id, target_id, rel_type):
        got = self.api.requests.post(self._baseurl, json={
            'source_id': source_id,
            'target_id': target_id,
            'type': rel_type})

        if not got.ok:
            raise SessionRqstError(resp=got, message=got.text)

        self.id = got.json()['id']
        return self

    def __str__(self):
        return json.dumps(self.value, indent=3)

    __repr__ = __str__
