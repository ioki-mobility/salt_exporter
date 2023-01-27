"""Simple Saltstack Highstate exporter
Report how many pending salt states from highstate are present based on output of
salt * -b {--batch-size} state.highstate test=True

This tool can only be used on the salt-master node.
"""
from wsgiref.simple_server import make_server
from prometheus_client import REGISTRY, make_wsgi_app
from salt import client

from .cli import params
from .collector import SaltHighstateCollector
from .logger import log


def main():
    # The LocalClient can only be run on the salt-master
    # https://docs.saltproject.io/en/latest/ref/clients/index.html#localclient
    caller = client.LocalClient()
    # Start up the server to expose the metrics.
    print(f"Listening on {params.listen_addr}:{params.listen_port}")

    REGISTRY.register(SaltHighstateCollector(caller, params, log))
    app = make_wsgi_app(REGISTRY)
    httpd = make_server(params.listen_addr, params.listen_port, app)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
