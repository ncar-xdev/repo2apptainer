from pkg_resources import DistributionNotFound, get_distribution
from repo2docker.app import Repo2Docker

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '0.0.0'


class Repo2Singularity(Repo2Docker):
    """
    An application for converting git repositories to singularity images.
    """

    name = 'repo2singularity'
    version = __version__
    description = __doc__

    def build_sif(self):
        from spython.main import Client

        self.sif_image = f'{self.output_image_spec}.sif'
        docker_uri = f'docker-daemon://{self.output_image_spec}:latest'
        image, builder = Client.build(docker_uri, image=self.sif_image, stream=True)
        print('\nBuilding singularity container from the built docker image...')
        print(image)

        for line in builder:
            print(line)

    def start(self):
        self.build()
        self.build_sif()
