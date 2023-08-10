from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import ValidationError
from dependencies import get_db
from db.schemas import QuizCreate, QuestionCreate, AnswerCreate
from db.crud import create_quiz, get_user_by_hash, get_quiz_by_id, get_questions_by_quiz_id
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


@quiz.post('/', response_class=HTMLResponse)
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
        response = RedirectResponse(request.url_for('create_question').include_query_params(quiz_id=db_quiz.id))
        return response
    except ValidationError as exc:
        context.update({'errors': [loc_by_exception(error) for error in exc.errors()]})
        context.update(**form)
    return get_template("create_quiz.html", context)


@quiz.get('/create/questions', response_class=HTMLResponse)
async def create_question_get(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for('lobby_get'))
    quiz_id = request.query_params.get('quiz_id')
    if not quiz_id:
        return back
    quiz = get_quiz_by_id(db, int(quiz_id))
    if not quiz:
        return back
    questions = get_questions_by_quiz_id(db, quiz_id)
    context = prepare_context(request)
    context.update({'quiz_id': quiz_id})
    context.update({'count': len(questions)})
    return get_template("create_question.html", context)


@quiz.post('/create/questions', response_class=HTMLResponse)
async def create_question_post(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for('lobby_get'))
    context = prepare_context(request)
    quiz_id = request.query_params.get('quiz_id')
    if not quiz_id:
        return back
    quiz = get_quiz_by_id(db, int(quiz_id))
    if not quiz:
        return back
    questions = get_questions_by_quiz_id(db, quiz_id)
    form = await form_to_obj(request)
    checked = any('check' in key for key in form.keys())
    if checked:
        context.update({"success": True})
    else:
        context.update({"error": True})
    context.update({'quiz_id': quiz_id})
    context.update({'count': len(questions)})
    return get_template("create_question.html", context)
