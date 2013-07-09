from flask import g

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

PLUGINS = {
    'cpu': cpu,
    'df': df,
}

def find_plugin(path):
    return path.split('.')[-1].split('-')[0]

def find_instance(path):
    return path.split('-')[-1]

def can_render(path):
    plugin = find_plugin(path)
    return plugin in PLUGINS

def get_render_urls(path, period='month'):
    plugin = find_plugin(path)
    return PLUGINS[plugin](path, period)
