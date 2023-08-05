import os
import logging

log = logging.getLogger(__name__)


def get_from_environment(variable, default):
    if variable in os.environ:
        v = os.environ.get(variable)
        log.info("Using environment variable %s=%s" % (variable, default))
    else:
        v = default
        log.warning("Using default variable %s=%s" % (variable, default))
    return v