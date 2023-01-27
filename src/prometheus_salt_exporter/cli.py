import argparse
from logging import WARN

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--listen-addr",
    help="Address to bind to",
    default="0.0.0.0"
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
    "--batch-size",
    type=int,
    help="Batch size to use in salt",
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
