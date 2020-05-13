import os
import subprocess
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution
from repo2docker.app import Repo2Docker

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '0.0.0'

SINGULARITY_CACHEDIR = os.environ.get('SINGULARITY_CACHEDIR', '~/.singularity/cache')
CACHEDIR_PATH = Path(SINGULARITY_CACHEDIR).expanduser()
if not CACHEDIR_PATH.exists():
    CACHEDIR_PATH.mkdir(exist_ok=True, parents=True)

REPO2SINGULARITY_CACHEDIR = CACHEDIR_PATH / 'repo2singularity'
REPO2SINGULARITY_CACHEDIR.mkdir(exist_ok=True, parents=True)


class Repo2Singularity(Repo2Docker):
    """
    An application for converting git repositories to singularity images.
    """

    name = 'repo2singularity'
    version = __version__
    description = __doc__

    def build_sif(self):
        from spython.main import Client

        self.singularity_image_name = f'{self.output_image_spec}.sif'
        self.sif_image = f'{REPO2SINGULARITY_CACHEDIR}/{self.singularity_image_name}'
        docker_uri = f'docker-daemon://{self.output_image_spec}:latest'
        image, builder = Client.build(docker_uri, image=self.sif_image, stream=True)
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
            f'library://andersy005/test/{self.output_image_spec}',
        ]
        run_command(cmd)

    def start(self):
        self.build()
        self.build_sif()
        if self.push:
            self.push_image()


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc
