import typer

from ._version import version as __version__
from .app import Repo2Singularity
from .console import console

app = typer.Typer(help='Convert a repository to a Singularity image')


def version_callback(value: bool):
    if value:
        typer.echo(f'Repo2Singularity Version: {__version__}')
        raise typer.Exit()


@app.command()
def build(repo: str, ref: str = 'main', force: bool = False):
    """Build a Singularity image from a repository"""
    console.print('Building a Singularity image from a repository')
    r2s = Repo2Singularity(repo=repo, ref=ref, force=force)
    console.print(f'Repository: {r2s.r2d.repo}')
    console.print(f'Reference: {r2s.r2d.ref}')
    console.print(f'Output image: {r2s.r2d.output_image_spec}')
    console.print(f'Cache directory: {r2s.cache_dir}')
    with console.status('Building docker image'):
        r2s.build_docker()
    with console.status('Building SIF image'):
        r2s.build_sif()
    console.print(f'SIF image: {r2s.sif_image}')


@app.command()
def run():
    """Run a Singularity image"""
    console.print('Running a Singularity image')


@app.command()
def version():
    """Print the version"""
    console.print(f'Repo2Singularity version: {__version__}')


def main():
    typer.run(app())
