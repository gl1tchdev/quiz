from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from dependencies import get_db
from db.schemas import QuizCreate
from db.crud import create_quiz
from db.crud import get_user_by_hash
from tools import *

quiz = APIRouter(prefix='/quiz')


@quiz.post('/', response_class=HTMLResponse)
async def lobby_post(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    context.update({'user': user})
    return get_template("lobby.html", context)


@quiz.get('/', response_class=HTMLResponse)
async def lobby_get(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    context.update({'user': user})
    return get_template("lobby.html", context)


@quiz.get('/', response_class=HTMLResponse)
async def lobby_post(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    return get_template("lobby.html", context)


@quiz.post('/search', response_class=HTMLResponse)
async def search(request: Request):
    context = prepare_context(request)
    return get_template("lobby.html", context)


@quiz.get('/create', response_class=HTMLResponse)
async def create_quiz_get(request: Request):
    context = prepare_context(request)
    return get_template("create_quiz.html", context)


@quiz.post('/create', response_class=HTMLResponse)
async def create_quiz_post(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    form = await form_to_obj(request)
    try:
        input_quiz = QuizCreate(**form, author_id=user.id)
        db_quiz = create_quiz(db, input_quiz)
        response = RedirectResponse(request.url_for('create_question').include_query_params(id=db_quiz.id))
        return response
    except ValidationError as exc:
        context.update({'errors': [loc_by_exception(error) for error in exc.errors()]})
        context.update(**form)
    return get_template("create_quiz.html", context)


@quiz.post('/create/questions', response_class=HTMLResponse)
async def create_question(request: Request):
    context = prepare_context(request)
    return get_template("create_question.html", context)
