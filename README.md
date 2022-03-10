# repo2apptainer

_✨ This code is highly experimental! Let the buyer beware ⚠️ ;) ✨_

| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![Code Coverage Status][codecov-badge]][codecov-link] [![pre-commit.ci status][pre-commit.ci-badge]][pre-commit.ci-link] |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                                                     [![Documentation Status][rtd-badge]][rtd-link]                                                                     |
| **Package** |                                                          [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                          |
| **License** |                                                                         [![License][license-badge]][repo-link]                                                                         |

Wrapper around [repo2docker](https://github.com/jupyter/repo2docker) producing Jupyter enabled [Apptainer/Singularity](https://apptainer.org/) images.

## Usage

```bash
$ repo2apptainer --help
Usage: repo2apptainer [OPTIONS] COMMAND [ARGS]...

  Convert a repository to a Apptainer (formerly Singularity) image

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  build    Build an Apptainer/Singularity image from a repository
  run      Run an Apptainer/Singularity image
  version  Print the version
```

```bash
$ repo2apptainer build --help
Usage: repo2apptainer build [OPTIONS] REPO

  Build an Apptainer/Singularity image from a repository

Arguments:
  REPO  [required]

Options:
  --ref TEXT            [default: main]
  --force / --no-force  [default: no-force]
  --help                Show this message and exit.
```

[github-ci-badge]: https://img.shields.io/github/workflow/status/ncar-xdev/repo2apptainer/CI?label=CI&logo=github
[github-ci-link]: https://github.com/ncar-xdev/repo2apptainer/actions?query=workflow%3ACI
[codecov-badge]: https://img.shields.io/codecov/c/github/ncar-xdev/repo2apptainer.svg?logo=codecov
[codecov-link]: https://codecov.io/gh/ncar-xdev/repo2apptainer
[rtd-badge]: https://img.shields.io/readthedocs/repo2apptainer/latest.svg
[rtd-link]: https://repo2apptainer.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/repo2apptainer?logo=pypi
[pypi-link]: https://pypi.org/project/repo2apptainer
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/repo2apptainer?logo=anaconda
[conda-link]: https://anaconda.org/conda-forge/repo2apptainer
[license-badge]: https://img.shields.io/github/license/ncar-xdev/repo2apptainer
[repo-link]: https://github.com/ncar-xdev/repo2apptainer
[pre-commit.ci-badge]: https://results.pre-commit.ci/badge/github/ncar-xdev/repo2apptainer/main.svg
[pre-commit.ci-link]: https://results.pre-commit.ci/latest/github/ncar-xdev/repo2apptainer/main
