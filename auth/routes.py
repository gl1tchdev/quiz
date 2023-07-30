from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError

from dependencies import *
from tools import *
from db import schemas, crud
from auth.password import verify_password

auth = APIRouter(prefix='/auth')


@auth.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Login'})
    return get_template('login.html', context)


@auth.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    context = prepare_context(request)
    context.update({'title': 'Sign up'})
    return get_template('signup.html', context)


@auth.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    form = await form_to_obj(request)
    try:
        user = schemas.UserLogin(**form)
        db_user = crud.get_user_by_login(db, user.login)
        if not db_user:
            context.update({'errors': 'login'})
        else:
            valid = verify_password(user.password, db_user.hashed_password)
            if valid:
                return RedirectResponse('/quiz')
            else:
                context.update({'errors': 'password'})
    except ValidationError as e:
        print(str(e))
    context.update(**form)
    context.update({'title': 'Login'})
    return get_template('login.html', context)


@auth.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, db: Session = Depends(get_db)):
    form = await form_to_obj(request)
    context = prepare_context(request)
    try:
        user = schemas.UserCreate(**form)
        db_user = crud.get_user_by_login(db, user.login)
        if db_user:
            return RedirectResponse(request.url_for('login_get').include_query_params(registered=True), status_code=303)
        else:
            crud.create_user(db, user)
            return RedirectResponse('/quiz')
    except ValidationError as exc:
        context.update({'errors': [loc_by_exception(error) for error in exc.errors()]})
    context.update(**form)
    context.update({'title': 'Sign up'})
    return get_template('signup.html', context)
