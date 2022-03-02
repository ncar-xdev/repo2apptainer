#!/usr/bin/env python3
# flake8: noqa
""" Top-level module for repo2singularity. """
from pkg_resources import DistributionNotFound, get_distribution

from .config import config

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    __version__ = '0.0.0'  # pragma: no cover
