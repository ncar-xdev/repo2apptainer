import getpass
import os
import socket
import subprocess
import tempfile
from pathlib import Path

from repo2docker.app import Repo2Docker
from repo2docker.utils import chdir

from . import __version__

SINGULARITY_CACHEDIR = os.environ.get('SINGULARITY_CACHEDIR', '~/.singularity/cache')
CACHEDIR_PATH = Path(SINGULARITY_CACHEDIR).expanduser()
if not CACHEDIR_PATH.exists():
    CACHEDIR_PATH.mkdir(exist_ok=True, parents=True)

REPO2SINGULARITY_CACHEDIR = CACHEDIR_PATH / 'repo2singularity'
REPO2SINGULARITY_CACHEDIR.mkdir(exist_ok=True, parents=True)
TMPDIR = tempfile.gettempdir()


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
        docker_uri = f'docker-daemon://{self.output_image_spec}:latest'
        cmd = ['singularity', 'build', '--force', self.sif_image, docker_uri]
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
            cmd = ['singularity', 'exec', '--writable', '--userns', self.sandbox_name]
            cmd += run_cmd
            self.log.info(
                f'{cmd}\n', extra=dict(phase='launching'),
            )
            subprocess.check_output(cmd)

    def run_image(self):
        """Run docker container from built image
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
                    '--force',
                    '--allow-unsigned',
                    '--dir',
                    REPO2SINGULARITY_CACHEDIR.as_posix(),
                    '--name',
                    self.singularity_image_name,
                    URI,
                ]
                self.log.info(
                    f'{cmd}\n', extra=dict(phase='pulling'),
                )
                subprocess.check_output(cmd)

                self.run_image()
            except Exception:
                pass

        self.build()
        self.build_sif()

        if self.push:
            self.push_image()
        if self.run:
            self.run_image()
