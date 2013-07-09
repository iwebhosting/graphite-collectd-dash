import requests
from urlparse import urlparse, urljoin
from urllib import urlencode

class Graphite(object):

    def __init__(self, url, prefix=None):
        self.url = urlparse(url).geturl()
        self.prefix = prefix

    def _make_url(self, path, args=None):
        url = urljoin(self.url, path)
        if args:
            url+= '?' + urlencode(args)
        return url

    def _make_query(self, query):
        parts = query.split('.')
        if self.prefix:
            if parts[0] != self.prefix:
                parts.insert(0, self.prefix)
        return '.'.join(parts)

    def get_nodes(self, query='*'):
        args = {
            'query': self._make_query(query),
            'contexts': 1,
            'node': 'GraphiteTree',
            'format': 'treejson',
        }
        resp = requests.get(self._make_url('metrics/find', args=args))
        return [h["text"] for h in resp.json() if h["expandable"]]

    def get_children(self, query):
        args = {
            'query': self._make_query(query),
            'contexts': 1,
            'node': 'GraphiteTree',
            'format': 'treejson',
        }
        resp = requests.get(self._make_url('metrics/expand', args=args))
        return [r.replace(query + '.', '') for r in resp.json()['results']]
