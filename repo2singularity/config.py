from __future__ import annotations

import pathlib

import donfig
import yaml

fn = pathlib.Path(__file__).parent / 'config.yaml'

with fn.open() as fobj:
    defaults = yaml.safe_load(fobj)

config = donfig.Config('repo2singularity', defaults=[defaults])
config.ensure_file(fn, comment=False)
