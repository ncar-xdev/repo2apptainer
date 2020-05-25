import os
import pathlib
import tempfile

SINGULARITY_CACHEDIR = os.environ.get('SINGULARITY_CACHEDIR', '~/.singularity/cache')
CACHEDIR_PATH = pathlib.Path(SINGULARITY_CACHEDIR).expanduser()
if not CACHEDIR_PATH.exists():
    CACHEDIR_PATH.mkdir(exist_ok=True, parents=True)

REPO2SINGULARITY_CACHEDIR = CACHEDIR_PATH / 'repo2singularity'
REPO2SINGULARITY_CACHEDIR.mkdir(exist_ok=True, parents=True)
TMPDIR = tempfile.gettempdir()
