from flask import g

def cpu(path, period):
    args = {}
    args['title'] = 'CPU Usage'
    args['areaMode'] = 'stacked'
    args['max'] = '100'
    targets = ['{}.*.value'.format(path),]
    return [g.graphite.get_graph_url(targets=targets, args=args, period=period)]

PLUGINS = {
    'cpu': cpu,
}

def find_plugin(path):
    return path.split('.')[-1].split('-')[0]

def can_render(path):
    plugin = find_plugin(path)
    return plugin in PLUGINS

def get_render_urls(path, period='month'):
    plugin = find_plugin(path)
    return PLUGINS[plugin](path, period)
    
