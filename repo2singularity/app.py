import getpass
import json
import os
import socket
import subprocess
from pathlib import Path

import requests
from repo2docker.app import Repo2Docker
from repo2docker.utils import chdir
from tqdm import tqdm

from . import __version__
from .cache import REPO2SINGULARITY_CACHEDIR, TMPDIR


class Repo2Singularity(Repo2Docker):
    """
    An application for converting git repositories to singularity images.
    """

    name = 'repo2singularity'
    version = __version__
    description = __doc__

    def build_sif(self):
        """
        Build Singularity Image File (SIF) from built docker image
        """
        if os.path.exists(self.sif_image) and not self.force:
            return
        docker_uri = f'docker-daemon://{self.output_image_spec}:latest'
        cmd = ['singularity', 'build']
        if self.force:
            cmd.append('--force')

        cmd.extend([self.sif_image, docker_uri])
        self.log.info(
            f'\nBuilding singularity container from the built docker image...\n{cmd}\n',
            extra=dict(phase='building'),
        )
        subprocess.check_output(cmd)

    def push_image(self):
        """
        Push Singularity image to registry
        """
        URI = f'library://{self.username_prefix}/{self.output_image_spec}:latest'

        self.log.info(
            f'Pushing image to {URI}\n', extra=dict(phase='pushing'),
        )
        cmd = [
            'singularity',
            'push',
            '-U',
            self.sif_image,
            URI,
        ]
        self.log.info(
            f'{cmd}', extra=dict(phase='pushing'),
        )
        subprocess.check_output(cmd)

    def create_container_sandbox(self):
        """
        Pre-convert the Singularity Image File (SIF) to a directory based format (sandbox)
        """

        self.log.info('Creating sandbox directory\n', extra=dict(phase='launching'))
        cmd = [
            'singularity',
            'build',
            '--force',
            '--sandbox',
            f'{TMPDIR}/{self.sandbox_name}',
            self.sif_image,
        ]
        self.log.info(
            f'{cmd}\n', extra=dict(phase='building'),
        )
        subprocess.check_output(cmd)

    def start_container(self):
        """
        Start singularity container from built image

        Returns running container
        """

        host_name = socket.gethostname()

        self.host_name = host_name
        if not self.run_cmd:
            port = str(self._get_free_port())
            ports = {f'{port}/tcp': port}
            user = getpass.getuser()
            run_cmd = [
                'jupyter',
                'lab',
                '--ip',
                self.host_name,
                '--port',
                port,
                f'--NotebookApp.custom_display_url=http://{host_name}:{port}',
                '--notebook-dir',
                f'/home/{user}',
            ]
        else:
            run_cmd = self.run_cmd
            if self.ports:
                ports = self.ports
            else:
                ports = {}
        self.ports = ports

        with chdir(Path(self.container_sandbox_dir).parent):
            cmd = ['singularity', 'exec', '--writable', '--userns']
            if self.bind:
                cmd.extend(['--bind', self.bind])

            cmd.append(self.sandbox_name)

            cmd += run_cmd
            self.log.info(
                f'{cmd}\n', extra=dict(phase='launching'),
            )
            subprocess.check_output(cmd)

    def run_image(self):
        """
        Run docker container from built image
        """

        self.create_container_sandbox()
        self.start_container()
        # TODO: wait for it to finish.

    def start(self):

        self.singularity_image_name = f'{self.output_image_spec}.sif'
        self.sif_image = f'{REPO2SINGULARITY_CACHEDIR}/{self.singularity_image_name}'
        self.sandbox_name = f'sandbox-{self.output_image_spec}'
        self.container_sandbox_dir = f'{TMPDIR}/{self.sandbox_name}'

        if self.run and os.path.exists(self.sif_image):
            self.run_image()

        elif self.run and self.username_prefix:
            try:
                URI = f'library://{self.username_prefix}/{self.output_image_spec}'
                cmd = [
                    'singularity',
                    'pull',
                    '--allow-unsigned',
                    '--dir',
                    REPO2SINGULARITY_CACHEDIR.as_posix(),
                    '--name',
                    self.singularity_image_name,
                ]

                if self.force:
                    cmd.append('--force')
                cmd.append(URI)
                self.log.info(
                    f'{cmd}\n', extra=dict(phase='pulling'),
                )
                subprocess.check_output(cmd)

                self.run_image()
            except Exception:
                pass

        if self.remote:
            if self.ref is None:
                ref = 'master'
            else:
                ref = self.ref
            data = {'url': self.repo, 'ref': ref, 'image_name': self.output_image_spec}
            downloader(data, self.sif_image, self.endpoint_url)

        else:
            self.build()
            self.build_sif()

        if self.push:
            self.push_image()
        if self.run:
            self.run_image()


def downloader(
    data: dict, output_file: str, endpoint_url: str, chunk_size: int = 2048,
):

    with requests.Session() as session:
        response = session.post(endpoint_url, data=json.dumps(data))
        response.raise_for_status()
        content = response.iter_content(chunk_size=chunk_size)
        total = int(response.headers.get('content-length', 0))
        progressbar = tqdm(
            total=total, ncols=82, unit='B', unit_scale=True, leave=True, desc='Downloading image'
        )
        with open(output_file, 'w+b') as fout:
            for chunk in content:
                if chunk:
                    fout.write(chunk)
                    fout.flush()
                    progressbar.update(chunk_size)
        progressbar.reset()
        progressbar.update(total)
        progressbar.close()
