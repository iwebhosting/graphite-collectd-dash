from flask import Blueprint, Flask, g, current_app
from graphite import Graphite

gcd = Blueprint('gcd', __name__)

@gcd.before_request
def setup_api():
    g.graphite = Graphite(current_app.config['GRAPHITE_URL'], 'collectd')

@gcd.route('/')
def browse_hosts():
    hosts = g.graphite.get_nodes()
    return ','.join(hosts)

@gcd.route('/host/<hostname>')
def host_detail(hostname):
    services = g.graphite.get_children(hostname + '.*')
    return ','.join(services)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(gcd)
    app.config['GRAPHITE_URL'] = 'http://collect2.manc.iws-hosting.co.uk/'
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
