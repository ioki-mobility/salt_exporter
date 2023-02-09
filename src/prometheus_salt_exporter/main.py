"""Simple Saltstack Highstate exporter
Report how many pending salt states from highstate are present based on output of
salt * -b {--batch-size} state.highstate test=True

This tool can only be used on the salt-master node.
"""
from prometheus_client import REGISTRY
from prometheus_client.twisted import MetricsResource
from salt import client
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from .cli import params
from .collector import SaltHighstateCollector
from .logger import log


def main():
    # The LocalClient can only be run on the salt-master
    # https://docs.saltproject.io/en/latest/ref/clients/index.html#localclient
    caller = client.LocalClient(auto_reconnect=True)
    # Start up the server to expose the metrics.
    print(f"Listening on {params.listen_addr}:{params.listen_port}")

    REGISTRY.register(SaltHighstateCollector(caller, params, log))

    root = Resource()
    root.putChild(b"metrics", MetricsResource(registry=REGISTRY))

    factory = Site(root)
    reactor.listenTCP(port=params.listen_port, factory=factory, interface=params.listen_addr)
    reactor.run()

if __name__ == "__main__":
    main()
