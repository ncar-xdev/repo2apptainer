from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/')
async def read_root():
    return 'Hello, World! Repo2singularity Remote Builder here.'


@app.post('/repos/{provider}/{org}/{repo}/{ref}')
async def repo(provider: str, org: str, repo: str, ref: str = None):
    providers = {'github': 'https://github.com', 'gh': 'https://github.com'}
    try:
        url = f'{providers[provider]}/{org}/{repo}'
    except KeyError:
        raise HTTPException(
            status_code=500,
            detail=f'Provider {provider} not found in list of valid providers {list(providers.keys())}',
        )

    return {'url': url}
