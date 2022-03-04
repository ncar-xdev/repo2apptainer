from __future__ import annotations

import pathlib
import subprocess

import pydantic
from repo2docker.app import Repo2Docker

from .config import config as _config
from .console import console
from .helpers import generate_image_name, resolve_ref


@pydantic.dataclasses.dataclass
class Repo2Apptainer:
    """An application for converting git repositories to Apptainer/Singularity images."""

    repo: str
    ref: str
    force: bool = False

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
        self.apptainer_image = (
            f"{_config.get('apptainer_in_docker.image')}:{_config.get('apptainer_in_docker.tag')}"
        )

    def build_docker(self) -> None:
        """Build docker image from repository"""
        with console.status('Building Docker image'):
            self.r2d.initialize()
            self.r2d.build()

    def build_sif(self) -> None:
        """Build Apptainer/Singularity Image File (SIF) from built docker image"""
        with console.status('Building Apptainer/Singularity image from the built docker image'):
            if not self.force and self.sif_image.exists():
                console.print(f'Skipping rebuild of {self.sif_image}')
            else:
                docker_uri = f'docker-daemon://{self.r2d.output_image_spec}:latest'
                cmd = [
                    'docker',
                    'run',
                    '--privileged',
                    '-v',
                    '/var/run/docker.sock:/var/run/docker.sock',
                    '-v',
                    f'{str(self.cache_dir)}:/work',
                    self.apptainer_image,
                    'build',
                    '--force',
                    self.sif_image.name,
                    docker_uri,
                ]

                console.print(cmd)
                subprocess.check_output(cmd)
