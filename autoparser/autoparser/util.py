"""
Common utility functions for autoparser
"""

DEFAULT_CONFIG = "config/redcap-en.toml"


def maybe(x, func, default=None):
    return func(x) if x is not None else default
