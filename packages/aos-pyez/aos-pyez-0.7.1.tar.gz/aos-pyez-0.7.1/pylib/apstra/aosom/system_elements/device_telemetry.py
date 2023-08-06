import retrying
import json

from apstra.aosom.exc import SessionRqstError
from apstra.aosom.utils.collection import Collection, CollectionItem


class DeviceTelemetryServiceItem(CollectionItem):

    def __init__(self, collection, name, datum):
        super(DeviceTelemetryServiceItem, self).__init__(
            collection, name, datum)

        self.input = ''
        self.interval = 10

    @property
    def current_data_raw(self):
        """
        Provides the telemetry data for this device/service

        Returns
        -------
        list
            raw data list of items returned by API (for now ...)
        """
        got = self.api.requests.get("%s/data" % self.url)
        if not got.ok:
            raise SessionRqstError(resp=got, message="""
            Unable to retrieve telemetry data
            """)
        return got.json()['items']

    @property
    def current_data(self):
        items = self.current_data_raw

        return {
            item['identity']: json.loads(item['actual']['value'])
            for item in items
        }

    def get(self):
        @retrying.retry(wait_fixed=1000, stop_max_delay=5000)
        def get_status():
            self.collection.digest()
            me = self.collection[self.name]
            assert me.value['status']
            return me.value

        self.datum = get_status()
        return self

    def start(self, input=None, interval=None):
        body = {
            'name': self.name,
            'input': input or self.input,
            'interval': interval or self.interval
        }

        got = self.api.requests.post(self.collection.url, json=body)
        if not got.ok:
            raise SessionRqstError(resp=got, message="""
            Unable to create/start service""")

        # for now, we need to re-digest the entire collection.
        # have asked for a 'get just this service' API. need to repeat
        # this process until we see the status value back from the API

        return self.get()

    def kill(self):
        got = self.api.requests.delete(self.url)
        if not got.ok:
            raise SessionRqstError(resp=got, message="""
            Unable to delete service""")

        self.collection.digest()
        self.datum = None
        return self

    def restart(self):
        self.kill()
        self.start()


class DeviceTelemetryServices(Collection):
    URI = 'services'
    LABEL = 'name'
    UNIQUE_ID = 'name'
    Item = DeviceTelemetryServiceItem

    def digest(self):
        """
        This method retrieves information about all known items within this collection.  A cache
        is then formed that provides an index by AOS unique ID, and another by user-defined
        item name.

        Returns: a list of all known items; each item is the dictionary of item data.
        """
        got = self.api.requests.get(self.url)
        if not got.ok:
            raise SessionRqstError(resp=got)

        body = got.json()

        self._cache.clear()
        self._cache['list'] = list()
        self._cache['names'] = list()
        self._cache['by_%s' % self.LABEL] = dict()
        self._cache['by_%s' % self.UNIQUE_ID] = dict()

        services = body['services']
        for item_name, item_data in services.items():
            self._add_item(item_data)
