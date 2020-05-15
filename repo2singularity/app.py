import os
import sys
import tempfile
from pathlib import Path

from repo2docker.app import Repo2Docker
from repo2docker.utils import chdir
from spython.main import Client
from spython.utils import get_username, stream_command

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
        docker_uri = f'docker-daemon://{self.output_image_spec}:latest'
        image, builder = Client.build(docker_uri, image=self.sif_image, stream=True, force=True)
        print('\nBuilding singularity container from the built docker image...')
        print(image)

        for line in builder:
            print(line)

    def push_image(self):
        """
        Push Singularity image to registry
        """

        self.log.info(
            'Pushing image\n', extra=dict(phase='pushing'),
        )

        cmd = [
            'singularity',
            'push',
            '-U',
            self.sif_image,
            f'library://andersy005/test/{self.output_image_spec}:latest',
        ]
        stream_command(cmd)

    def create_container_sandbox(self):
        """
        Pre-convert the Singularity Image File (SIF) to a directory based format (sandbox)
        """
        image, builder = Client.build(
            image=self.sandbox_name,
            recipe=self.sif_image,
            build_folder=TMPDIR,
            sandbox=True,
            sudo=False,
            stream=True,
            force=True,
        )
        print(image)
        for line in builder:
            try:
                print(line)
            except Exception:
                sys.exit(0)

    def start_container(self):
        """
        Start singularity container from built image

        Returns running container
        """

        host_name = '127.0.0.1'

        self.host_name = host_name
        if not self.run_cmd:
            port = str(self._get_free_port())
            ports = {f'{port}/tcp': port}
            user = get_username()
            run_cmd = [
                'jupyter',
                'lab',
                '--ip',
                '0.0.0.0',
                '--port',
                port,
                f'--NotebookApp.custom_display_url=http://{host_name}:{port}',
                '--notebook-dir',
                f'{self.container_sandbox_dir}/home/{user}',
            ]
        else:
            run_cmd = self.run_cmd
            if self.ports:
                ports = self.ports
            else:
                ports = {}
        self.ports = ports

        with chdir(Path(self.container_sandbox_dir).parent):
            executor = Client.execute(
                image=self.sandbox_name, writable=True, command=run_cmd, stream=True, quiet=False
            )
            for line in executor:
                try:
                    print(line)
                except Exception:
                    sys.exit(0)

    def run_image(self):
        """Run docker container from built image
        """

        self.create_container_sandbox()
        self.start_container()
        # TODO: wait for it to finish.

    def start(self):
        self.build()
        self.singularity_image_name = f'{self.output_image_spec}.sif'
        self.sif_image = f'{REPO2SINGULARITY_CACHEDIR}/{self.singularity_image_name}'
        self.sandbox_name = f'sandbox-{self.output_image_spec}'
        self.container_sandbox_dir = f'{TMPDIR}/{self.sandbox_name}'
        self.build_sif()
        if self.push:
            self.push_image()
        if self.run:
            self.run_image()
