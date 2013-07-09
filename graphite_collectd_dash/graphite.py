import requests
from urlparse import urlparse, urljoin
from urllib import urlencode

periods = {
    'hour': '-60minutes',
    'day': '-24hours',
    'week': '-7days',
    'month': '-30days',
    'year': '-365days',
}

basic_graph = {
    'width': 800,
    'until': 'now',
    'height': 250,
    'fontName': 'Sans',
    'lineMode': 'connected',
    'hideLegend': 'false',
    'fontBold': 'true',
    'bgcolor': 'FFFFFF',
    'fgcolor': '000000',
}


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

    def get_graph_url(self, targets, args, period='month'):
        d = basic_graph.copy()
        d['from'] = periods[period]
        args = d.items()
        args = args + [('target', target) for target in targets]
        return self._make_url('render', args=args)
