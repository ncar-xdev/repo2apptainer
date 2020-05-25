import subprocess

from fastapi import FastAPI
from pydantic import BaseModel


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
    subprocess.check_call(command)
    return command
