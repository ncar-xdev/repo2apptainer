import typer
from repo2docker import __version__ as __repo2docker_version__

from ._version import version as __version__
from .app import Repo2Apptainer
from .console import console
from .helpers import resolve_ref

app = typer.Typer(help='Convert a repository to a Apptainer (formerly Singularity) image')


def version_callback(value: bool):
    if value:
        typer.echo(f'Repo2Apptainer Version: {__version__}')
        typer.echo(f'Repo2Docker version   : {__repo2docker_version__}')
        raise typer.Exit()


@app.command()
def build(repo: str, ref: str = 'main', force: bool = False):
    """Build an Apptainer/Singularity image from a repository"""
    console.print('Building an Apptainer/Singularity image from a repository')
    ref = resolve_ref(repo, ref) if ref is None else ref
    r2s = Repo2Apptainer(repo=repo, ref=ref, force=force)
    console.print(f'Repository: {r2s.r2d.repo}')
    console.print(f'Reference: {r2s.r2d.ref}')
    console.print(f'Output image: {r2s.r2d.output_image_spec}')
    console.print(f'Cache directory: {r2s.cache_dir}')
    r2s.build_docker()
    r2s.build_sif()
    console.print(f'SIF image: {r2s.sif_image}')


@app.command()
def run():
    """Run an Apptainer/Singularity image"""
    console.print('Running an Apptainer/Singularity image')


@app.command()
def version():
    """Print the version"""
    console.print(f'Repo2Apptainer version: {__version__}')
    console.print(f'Repo2Docker version   : {__repo2docker_version__}')


def main():
    typer.run(app())
