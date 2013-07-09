from flask import Blueprint, Flask, g, current_app, render_template, request
from graphite import Graphite
from render import can_render, get_render_urls

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
    s = g.graphite.get_children(hostname + '.*')
    return render_template('detail.html', hostname=hostname, period=p, services=s)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(gcd)
    app.config['GRAPHITE_URL'] = 'http://collect2.manc.iws-hosting.co.uk/'
    app.jinja_env.globals.update(can_render=can_render)
    app.jinja_env.globals.update(get_render_urls=get_render_urls)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
