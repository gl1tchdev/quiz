from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from auth.routes import auth
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    app.include_router(auth)
    app.mount('/', StaticFiles(directory="static"), name="static")
    return app

app = create_app()

