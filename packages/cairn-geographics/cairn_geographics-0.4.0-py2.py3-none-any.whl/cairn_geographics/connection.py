import cairn_geographics
from cairn_geographics.gis_object import CairnGisObject
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

if os.environ.get('CAIRN_GIS_LOCAL_MODE') == '1':
    CAIRN_GEOGRAPHICS_DEFAULT_URL = 'localhost:4000'
else:
    CAIRN_GEOGRAPHICS_DEFAULT_URL = 'https://www.cairngeographics.com'

BATCH_SIZE = 500

class Connection(object):
    def __init__(self, api_token, cairn_geographics_url = None):
        assert api_token.startswith('CGIS-'), 'Cairn Geographics requires a valid API token; visit www.cairngis.com to sign up for free.'
        self.api_token = api_token
        if cairn_geographics_url is None:
            cairn_geographics_url = CAIRN_GEOGRAPHICS_DEFAULT_URL
        self.cairn_geographics_url = self.get_api_url(cairn_geographics_url)
        self.api_version = self.get_api_version()

    def get_api_url(self, cairn_geographics_url):
        api_url = ""
        # Add https:// in front of URL if necessary; required for requests module.
        if not cairn_geographics_url.startswith("https://"):
            api_url += "https://"

        # Remove trailing /
        if cairn_geographics_url.endswith("/"):
            api_url += cairn_geographics_url[:-1]
        else:
            api_url += cairn_geographics_url

        # Add /api if not already present
        if not api_url.endswith("/api"):
            api_url += "/api"
        return api_url

    def get_api_version(self):
        response = requests.get(self.cairn_geographics_url, verify=False)
        response.raise_for_status()
        response_json = response.json()
        if 'version' not in response_json:
            raise ValueError("Did not receive API version from CairnGis server.")
        return response_json['version']

    def run(self, query):
        if isinstance(query, CairnGisObject):
            return self._run_single(query)
        elif hasattr(query, '__iter__'):
            return self._run_batched_queries(query)
        else:
            raise ValueError('Expected either Cairn Geographics query or iterable of Cairn Geographics queries.')

    def _run_single(self, query):
        payload = {'q': query.compile(), 'token': self.api_token}
        response = requests.get(self.cairn_geographics_url + "/query", params=payload, verify=False)

        if response.status_code == 400:
            raise RuntimeError(response.json()['message'])
        else:
            response.raise_for_status()

        result = response.json()
        return getattr(cairn_geographics, result['type']).from_dict(result)

    @staticmethod
    def _grouper(iterable, n):
        args = [iter(iterable)] * n
        return list(zip_longest(*args, fillvalue=None))

    def _run_batched_queries(self, batched_queries):
        batches = self._grouper(map(lambda x: x.compile(), batched_queries), BATCH_SIZE)

        for batch in batches:
            payload = {'q': [query for query in batch if query is not None], 'token': self.api_token}
            response = requests.post(self.cairn_geographics_url + "/batched_query", json=payload)

            if response.status_code == 400:
                raise RuntimeError(response.json()['message'])
            else:
                response.raise_for_status()

            result = response.json()
            for item in result:
                yield getattr(cairn_geographics, item['type']).from_dict(item)
