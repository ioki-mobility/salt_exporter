import logging

from .cli import params

log_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

# Salt overrides Python logging, hence we have to use our own handler
# for logging to work as expected
log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(params.log_level)
ch.setFormatter(log_formatter)
log.addHandler(ch)
