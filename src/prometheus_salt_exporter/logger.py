import logging
import sys

from .cli import params

log = logging.getLogger(__name__)
log.propagate = False
log.setLevel(params.log_level)
stdout_handler = logging.StreamHandler(sys.stdout)
log.addHandler(stdout_handler)
