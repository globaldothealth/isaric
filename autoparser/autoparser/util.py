"""
Common utility functions for autoparser
"""

from typing import Optional, Dict, Any

DEFAULT_CONFIG = "redcap-en.toml"


def maybe(x, func, default=None):
    return func(x) if x is not None else default
