from fastapi import FastAPI
from auth.routes import auth
from fastapi.staticfiles import StaticFiles
from db import models
from db.database import engine


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None)
    app.include_router(auth)
    app.mount('/', StaticFiles(directory="static"), name="static")
    models.Base.metadata.create_all(bind=engine)
    return app

app = create_app()

