from __future__ import annotations

import subprocess

import escapism


def resolve_ref(repo_url: str, ref: str) -> str:
    """
    Return resolved commit hash for branch / tag.
    Return ref unmodified if branch / tag isn't found

    Parameters
    ----------
    repo_url : str
        URL of the repository
    ref : str
        Branch / tag to resolve

    Returns
    -------
    resolved_ref : str

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


def generate_image_name(repo: str, resolved_ref: str) -> str:
    """Generate an image name for the repo + ref

    Parameters
    ----------
    repo : str
        repository URL
    resolved_ref : str
        resolved git repo reference

    Returns
    -------
    image_name : str
        image name
    """

    return f'r2s-{escapism.escape(repo, escape_char="-").lower()}-{resolved_ref}'
