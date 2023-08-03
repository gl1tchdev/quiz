from fastapi import FastAPI, Request, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated, Union
from auth.routes import auth
from quiz.routes import quiz
from db import models
from db.database import engine


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None)
    app.include_router(auth)
    app.include_router(quiz)
    app.mount('/static', StaticFiles(directory="static"), name="static")
    models.Base.metadata.create_all(bind=engine)
    return app


app = create_app()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, hash: Annotated[Union[str, None], Cookie()] = None):
    if hash:
        response = RedirectResponse(request.url_for('lobby'))
    else:
        response = RedirectResponse(request.url_for('login_get'))
    return response

@app.get('/logout')
async def logout_copy(request: Request):
    return RedirectResponse(request.url_for('logout'))

@app.get('/login')
async def login_copy(request: Request):
    return RedirectResponse(request.url_for('login_get'))

@app.get('/signup')
async def signup_copy(request:Request):
    return RedirectResponse(request.url_for('signup_get'))