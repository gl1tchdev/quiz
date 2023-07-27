from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from dependencies import *


auth = APIRouter(prefix='/auth')


@auth.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Login'})
    return get_template('login.html', context)

@auth.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Login'})
    return get_template('login.html', context)

@auth.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Sign up'})
    return get_template('signup.html', context)

@auth.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Sign up'})
    return get_template('signup.html', context)

