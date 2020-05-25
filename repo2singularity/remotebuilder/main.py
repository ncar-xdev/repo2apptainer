import os
import subprocess

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from repo2singularity.cache import REPO2SINGULARITY_CACHEDIR


class Repo(BaseModel):
    url: str
    ref: str = None
    image_name: str


app = FastAPI()


@app.get('/')
async def read_root():
    return 'Hello, World! Repo2singularity Remote Builder here.'


@app.post('/repo/')
async def repo(repo: Repo):
    command = ['repo2singularity', '--image-name', repo.image_name]
    if repo.ref:
        command.extend(['--ref', repo.ref])
    command.append(repo.url)

    image_path = f'{REPO2SINGULARITY_CACHEDIR}/{repo.image_name}.sif'
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        subprocess.check_call(command)
        return FileResponse(image_path)
