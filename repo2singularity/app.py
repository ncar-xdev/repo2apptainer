from __future__ import annotations

import pathlib
import subprocess

import pydantic
from repo2docker.app import Repo2Docker

from .config import config as _config
from .console import console
from .helpers import generate_image_name, resolve_ref


@pydantic.dataclasses.dataclass
class Repo2Singularity(Repo2Docker):
    repo: str
    ref: str
    rebuild: bool = False

    def __post_init__(self) -> None:
        self.cache_dir = pathlib.Path(
            _config.get('cache_dir') or pathlib.Path.home() / '.singularity/cache'
        ).resolve()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.r2d = Repo2Docker()
        self.r2d.repo = self.repo
        self.r2d.ref = resolve_ref(self.repo, self.ref)
        self.r2d.output_image_spec = generate_image_name(self.repo, self.r2d.ref)
        self.sif_image = self.cache_dir / f'{self.r2d.output_image_spec}.sif'

    def build(self) -> None:
        self.r2d.initialize()
        self.r2d.build()

        if not self.rebuild and self.sif_image.exists():
            console.log(f'Skipping rebuild of {self.sif_image}')

        else:
            docker_uri = f'docker-daemon://{self.r2d.output_image_spec}:latest'
            cmd = ['singularity', 'build', '--force', str(self.sif_image), docker_uri]
            console.log('Building singularity image from the built docker image')
            console.log(cmd)
            subprocess.check_output(cmd)
