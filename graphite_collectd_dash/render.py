from flask import g
from collections import defaultdict

def cpu(path, period):
    args = {}
    args['title'] = 'CPU Usage'
    args['areaMode'] = 'stacked'
    args['max'] = '100'
    targets = ['{}.*.value'.format(path),]
    return [g.graphite.get_graph_url(targets=targets, args=args, period=period)]

def df(path, period):
    args = {}
    args['areaMode'] = 'stacked'
    fs = g.graphite.get_children(path + '.*')
    t_paths = ['{}.*'.format(f) for f in fs]
    res = []
    for p in t_paths:
        a = args.copy()
        a['title'] = 'Disk space on {}'.format(find_instance(p))
        res.append(
            g.graphite.get_graph_url(targets=[p, ], args=a, period=period)
        )
    return res

def interface(path, period):
    args = {}
    children = g.graphite.get_children(path + '.*')
    args['height'] = 250 + (10 * len(children))
    targets = []
    res = []
    for child in children:
        if 'octet' not in child: continue
        dev = child.split('.')[-1].split('-')[1]
        targets = []
        for i in ['tx', 'rx']:
            targets += ["cactiStyle(alias(scale({}.{}, 0.000008), '{} {}'))".format(child, i, dev, i),]
            targets += ["cactiStyle(alias(nPercentile(scale(summarize(sum({}.{}), '5min', 'max'), 0.000008), 95), '{} {} 95th'))".format(child, i, dev, i),]
        res.append(g.graphite.get_graph_url(targets=targets, args=args, period=period))
    return res

def have_a_go(path, period):
    args = {}
    children = g.graphite.get_children(path + '.*.*')
    args['height'] = 250 + (10 * len(children))
    targets = ['{}.*.*'.format(path),]
    return [g.graphite.get_graph_url(targets=targets, args=args, period=period)]

PLUGINS = defaultdict(lambda:  have_a_go)

PLUGINS.update({
    'cpu': cpu,
    'df': df,
    'interface': interface,
})

def find_plugin(path):
    return path.split('.')[-1].split('-')[0]

def find_instance(path):
    return path.split('-')[-1]

def get_render_urls(path, period='month'):
    plugin = find_plugin(path)
    return PLUGINS[plugin](path, period)
