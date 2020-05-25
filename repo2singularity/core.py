import logging
import subprocess

import escapism
import typer
from repo2docker.utils import is_valid_docker_image_name

from repo2singularity.app import Repo2Singularity

from . import __version__


def resolve_ref(repo_url, ref):
    """
    Return resolved commit hash for branch / tag.
    Return ref unmodified if branch / tag isn't found

    Notes
    -----

    Author: Yuvi Panda
    Copied from https://github.com/yuvipanda/repo2charliecloud/blob/
               44a508b632e801d3b1f0dd1360e38f73d80efc74/repo2charliecloud/__init__.py#L6
    """
    stdout = subprocess.check_output(['git', 'ls-remote', repo_url]).decode()
    # ls-remote output looks like this:
    # <hash>\t<ref>\n
    # <hash>\t<ref>\n
    # Since our ref can be a tag (so refs/tags/<ref>) or branch
    # (so refs/head/<ref>), we get all refs and check if either
    # exists
    all_refs = [line.split('\t') for line in stdout.strip().split('\n')]
    for git_hash, ref in all_refs:
        if ref in (f'refs/heads/{ref}', f'refs/heads/{ref}'):
            return git_hash[:7]  # Return first 7 characters

    if stdout:
        return stdout.split()[0][:7]
    return ref[:7]


def generate_image_name(repo, resolved_ref):
    """Generate an image name for the repo + ref

    Parameters
    ----------
    repo : str
        repository URL
    resolved_ref : str
        resolved git repo reference
    """

    return f'r2s-{escapism.escape(repo, escape_char="-").lower()}-{resolved_ref}'


def version_callback(value: bool):
    if value:
        typer.echo(f'repo2singularity version: {__version__}')
        raise typer.Exit()


def validate_image_name(image_name):
    """
    Validate image_name read by typer.

    Notes
    -----

    Container names must start with an alphanumeric character and
    can then use _ . or - in addition to alphanumeric.
    [a-zA-Z0-9][a-zA-Z0-9_.-]+

    Parameters
    -----------
    image_name : str
             argument read by the argument parser

    Returns
    --------
         unmodified image_name
    Raises
    ------

    TypeError:

        if image_name contains characters that do not
        meet the logic that container names must start
        with an alphanumeric character and can then
        use _ . or - in addition to alphanumeric.
        [a-zA-Z0-9][a-zA-Z0-9_.-]+
    """
    if not image_name:
        return image_name
    elif not is_valid_docker_image_name(image_name):
        msg = (
            f'{image_name} is not a valid image name. Image name '
            'must start with an alphanumeric character and '
            'can then use _ . or - in addition to alphanumeric.'
        )
        raise TypeError(msg)
    return image_name


def cli(
    repo: str,
    ref: str = typer.Option(
        'master', show_default=True, help='Remote repository reference to build.'
    ),
    image_name: str = typer.Option(
        '',
        show_default=True,
        help='Name of image to be built. If unspecified will be autogenerated.',
        callback=validate_image_name,
    ),
    push: bool = typer.Option(
        False, show_default=True, help='Push singularity image to image registry.'
    ),
    username_prefix: str = typer.Option(
        '',
        show_default=True,
        help=(
            'Username and prefix to use when constructing image URI before pushing it to or pulling it from the registry. '
            'For example, user/prefix: `milkshake/chocolate`. Used in conjunction with --push and --run (to pull existing image).'
        ),
    ),
    run: bool = typer.Option(
        False, show_default=True, help='Run container after it has been built.'
    ),
    bind: str = typer.Option(
        '',
        show_default=True,
        help=(
            'Volumes to mount inside the container, in form '
            'src[:dest[:opts]], where src and dest are outside and inside paths.  If dest '
            "is not given, it is set equal to src. Mount options ('opts') may be specified as "
            "'ro' (read-only) or 'rw' (read/write, which is the default)"
        ),
    ),
    json_logs: bool = typer.Option(
        False, show_default=True, help='Emit JSON logs instead of human readable logs.'
    ),
    debug: bool = typer.Option(False, show_default=True, help='Turn on debug logging.'),
    remote: bool = typer.Option(False, show_default=True, help='build image remotely'),
    version: bool = typer.Option(
        None,
        '--version',
        callback=version_callback,
        is_eager=True,
        help='Print the repo2singularity version and exit.',
    ),
):
    """
    Fetch a repository and build a singularity image.
    """
    resolved_ref = resolve_ref(repo, ref)
    r2s = Repo2Singularity()
    r2s.repo = repo
    r2s.ref = ref
    if image_name:
        r2s.output_image_spec = image_name
    else:
        r2s.output_image_spec = generate_image_name(repo, resolved_ref)

    r2s.json_logs = json_logs
    r2s.run = run
    r2s.bind = bind
    if debug:
        r2s.log_level = logging.DEBUG

    if push and not username_prefix:
        raise ValueError('Missing `user/prefix component for the image URI.')
    r2s.push = push
    r2s.remote = remote
    r2s.username_prefix = username_prefix
    r2s.initialize()
    r2s.start()


def main():
    return typer.run(cli)
