import argparse
from logging import WARN

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--listen-addr",
    help="Address to bind to. IPv4 and IPv6 addresses can be specified.",
    default="::"
)
parser.add_argument(
    "--listen-port",
    type=int,
    help="Port to bind to",
    default=9175
)
parser.add_argument(
    "--highstate-interval",
    type=int,
    help="Seconds between each highstate test run",
    default=300
)
parser.add_argument(
    "--wait-on-error-interval",
    type=int,
    help="Seconds to wait when an error occurs (e.g. salt-master not responding in time)",
    default=300
)
parser.add_argument(
    "--batch-size",
    type=int,
    help="Batch size to use in salt",
    default=10
)
parser.add_argument(
    "--batch-wait",
    type=int,
    help="Seconds to wait after a minion returns, before sending the command to a new minion",
    default=10
)
parser.add_argument(
    "--salt-target",
    type=str,
    help="Salt target to be used",
    default="*"
)
parser.add_argument(
    "--log-level",
    help="log level",
    default=WARN
)
params = parser.parse_args()
