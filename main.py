from pathlib import Path

import fastapi
import fastapi_chameleon
import uvicorn
from starlette.staticfiles import StaticFiles

from data import db_session
from views import home
from views import account
from views import packages

app = fastapi.FastAPI()


def main():
    config()
    uvicorn.run(app, host='127.0.0.1', port=8000)


def config(dev_mode=bool):
    config_template(dev_mode)
    config_route()
    config_db(dev_mode)


def config_template(dev_mode=bool):
    fastapi_chameleon.global_init('./templates', auto_reload=dev_mode)


def config_db(dev_mode=bool):
    file = (Path(__file__).parent / 'db' / 'pypi.sqlite').absolute()
    db_session.global_init(file.as_posix())


def config_route():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(home.router)
    app.include_router(account.router)
    app.include_router(packages.router)


if __name__ == '__main__':
    main()
else:
    config(dev_mode=True)
