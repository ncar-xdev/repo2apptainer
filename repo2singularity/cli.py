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
def build(repo: str, ref: str = 'main', rebuild: bool = False):
    """Build a Singularity image from a repository"""
    console.log('Building a Singularity image from a repository')
    r2s = Repo2Singularity(repo=repo, ref=ref, rebuild=rebuild)
    console.log(f'Repository: {r2s.r2d.repo}')
    console.log(f'Reference: {r2s.r2d.ref}')
    console.log(f'Output image: {r2s.r2d.output_image_spec}')
    console.log(f'SIF image: {r2s.sif_image}')
    console.log(f'Cache directory: {r2s.cache_dir}')
    with console.status('Building docker image'):
        r2s.build()


@app.command()
def run():
    """Run a Singularity image"""
    console.log('Running a Singularity image')


@app.command()
def version():
    """Print the version"""
    console.print(f'Repo2Singularity version: {__version__}')


def main():
    typer.run(app())
