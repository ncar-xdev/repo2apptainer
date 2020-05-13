from repo2docker.app import Repo2Docker


class Repo2Singularity(Repo2Docker):
    """
    An application for converting git repositories to singularity images.
    """

    name = 'repo2singularity'
    version = '0.0.1'
    description = __doc__

    def start(self):
        self.build()
