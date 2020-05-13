#!/usr/bin/env python3
""" Top-level module for repo2singularity. """
# Import intake first to avoid circular imports during discovery.
from pkg_resources import DistributionNotFound, get_distribution
from .app import Repo2Singularity  # noqa: F401

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # noqa: F401
    __version__ = '0.0.0'
