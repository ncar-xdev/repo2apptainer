from repo2docker.app import Repo2Docker


class Repo2Singularity(Repo2Docker):
    """
    An application for converting git repositories to singularity images.
    """

    name = 'repo2singularity'
    version = '0.0.1'
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
