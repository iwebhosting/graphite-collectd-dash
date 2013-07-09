from flask import g

def cpu(path, period):
    urls = []
    return urls

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
    
