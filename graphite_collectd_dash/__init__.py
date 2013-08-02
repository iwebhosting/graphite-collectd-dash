from flask import Blueprint, Flask, g, current_app, render_template, request
from graphite import Graphite
from render import get_render_urls
import os
import re

gcd = Blueprint('gcd', __name__)

@gcd.before_request
def setup_api():
    g.graphite = Graphite(current_app.config['GRAPHITE_URL'], 'collectd')

@gcd.route('/')
def browse_hosts():
    hosts = g.graphite.get_nodes()
    return render_template('hosts.html', hosts=hosts)

@gcd.route('/host/<hostname>')
def host_detail(hostname):
    p = request.args.get('period', 'month')
    all_machines = g.graphite.get_children('*')
    r = re.compile(hostname)
    s = []
    for machine in [machine for machine in all_machines if r.search(machine)]:
        s += g.graphite.get_children(machine + '.*')
    return render_template('detail.html', hostname=hostname, period=p, services=s)

@gcd.route('/host/<hostname>/<graph>')
def host_graph_detail(hostname, graph):
    p = request.args.get('period', 'month')
    all_machines = g.graphite.get_children('*')
    r = re.compile(hostname)
    gr = re.compile(graph)
    s = []
    for machine in [machine for machine in all_machines if r.search(machine)]:
        ss = g.graphite.get_children(machine + '.*')
        s += [x for x in ss if gr.search(x.split('.')[2])]
    return render_template('detail.html', hostname=hostname, period=p, services=s)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(gcd)
    app.config['GRAPHITE_URL'] = os.environ.get('GRAPHITE_URL')
    if app.config['GRAPHITE_URL'] is None:
        raise RuntimeError('GRAPHITE_URL env must be set')
    app.jinja_env.globals.update(get_render_urls=get_render_urls)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
