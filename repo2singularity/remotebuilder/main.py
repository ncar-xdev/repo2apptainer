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
    if not os.path.exists(image_path):
        await build_image(command)

    return FileResponse(image_path, media_type='application/octet-stream')


async def build_image(command):
    subprocess.check_call(command)
