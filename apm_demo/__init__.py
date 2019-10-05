from ddtrace import patch_all, config

config.trace_headers([
    'User-Agent',
    'content-length'
])
patch_all()

from .app import app, db  # noqa
