from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from auth.routes import auth
from quiz.routes import quiz
from db import models, crud
from db.database import engine
from tools import *


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None)
    app.include_router(auth)
    app.include_router(quiz)
    app.mount('/static', StaticFiles(directory="static"), name="static")
    models.Base.metadata.create_all(bind=engine)
    return app


app = create_app()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(request.url_for('login_get'))


@app.get('/logout')
async def logout_copy(request: Request):
    return RedirectResponse(request.url_for('logout'))


@app.get('/login')
async def login_copy(request: Request):
    return RedirectResponse(request.url_for('login_get'))


@app.get('/signup')
async def signup_copy(request: Request):
    return RedirectResponse(request.url_for('signup_get'))


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    path = str(request.url.path)
    cookie = request.cookies.get('hash')
    awaited_response = await call_next(request)
    if not (cookie or 'auth' in path) and all(x not in path for x in ['logout', 'static']):
        return RedirectResponse(request.url_for('login_get'))
    if cookie and 'auth' in path and 'logout' not in path:
        return RedirectResponse(request.url_for('lobby_get'))
    return awaited_response
