from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import ValidationError
from dependencies import get_db
from db.schemas import QuizCreate, QuestionCreate, AnswerCreate
from db.crud import *
from tools import *

quiz = APIRouter(prefix='/quiz')


@quiz.post('/', response_class=HTMLResponse)
async def lobby_post(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    context.update({'user': user})
    context.update({'page_title': 'Lobby'})
    if request.query_params.get('created'):
        context.update({'created': True})
    quiz_list = get_quiz_list(db)
    if len(quiz_list) != 0:
        context.update({'quiz_list': quiz_list})
    return get_template("lobby.html", context)


@quiz.get('/', response_class=HTMLResponse)
async def lobby_get(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    context.update({'user': user})
    if request.query_params.get('created'):
        context.update({'created': True})
    context.update({'page_title': 'Lobby'})
    quiz_list = get_quiz_list(db)
    if len(quiz_list) != 0:
        context.update({'quiz_list': quiz_list})
    return get_template("lobby.html", context)


@quiz.post('/', response_class=HTMLResponse)
async def lobby_post(request: Request):
    context = prepare_context(request)
    if request.query_params.get('created'):
        context.update({'created': True})
    context.update({'page_title': 'Lobby'})
    return get_template("lobby.html", context)


@quiz.post('/search', response_class=HTMLResponse)
async def search(request: Request):
    context = prepare_context(request)
    context.update({'page_title': 'Lobby'})
    return get_template("lobby.html", context)


@quiz.get('/create', response_class=HTMLResponse)
async def create_quiz_get(request: Request):
    context = prepare_context(request)
    context.update({'page_title': 'Create quiz'})
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
        response = RedirectResponse(request.url_for('create_question_get').include_query_params(quiz_id=db_quiz.id))
        return response
    except ValidationError as exc:
        context.update({'errors': [loc_by_exception(error) for error in exc.errors()]})
        context.update(**form)
    context.update({'page_title': 'Create quiz'})
    return get_template("create_quiz.html", context)


@quiz.get('/create/questions', response_class=HTMLResponse)
async def create_question_get(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for('lobby_get'))
    quiz_id = request.query_params.get('quiz_id')
    if not quiz_id:
        return back
    quiz_id = int(quiz_id)
    quiz = get_quiz_by_id(db, quiz_id)
    if not quiz:
        return back
    questions = get_questions_by_quiz_id(db, quiz_id)
    if len(questions) == 5:
        return back
    context = prepare_context(request)
    context.update({'quiz_id': quiz_id})
    context.update({'count': len(questions)})
    context.update({'page_title': 'Create question'})
    return get_template("create_question.html", context)


@quiz.post('/create/questions', response_class=HTMLResponse)
async def create_question_post(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for('lobby_get'))
    context = prepare_context(request)
    quiz_id = request.query_params.get('quiz_id')
    if not quiz_id:
        return back
    quiz_id = int(quiz_id)
    quiz = get_quiz_by_id(db, quiz_id)
    if not quiz:
        return back
    questions = get_questions_by_quiz_id(db, quiz_id)
    if len(questions) == 5:
        return back
    form = await form_to_obj(request)
    checked = any('check' in key for key in form.keys())
    if checked:
        form_dict = question_form_to_dict(form)
        question_text = form_dict[0]
        question_schema = QuestionCreate(text=question_text, quiz_id=quiz_id)
        db_question = create_question(db, question_schema, quiz_id)
        answers_dict = form_dict[1]
        answers = []
        for answer in answers_dict:
            answer_schema = AnswerCreate(text=answer['text'], question_id=db_question.id, is_correct=answer['is_correct'])
            answers.append(answer_schema)
        db_answers = create_answers(db, answers, db_question.id)
        context.update({"success": True})

    else:
        context.update({"error": True})
    context.update({'quiz_id': quiz_id})
    questions = get_questions_by_quiz_id(db, quiz_id)
    question_len = len(questions)
    if question_len == 5:
        return RedirectResponse(request.url_for('lobby_get').include_query_params(created=True))
    else:
        context.update({'count': len(questions)})
    context.update({'page_title': 'Create question'})
    return get_template("create_question.html", context)


@quiz.get('/show', response_class=HTMLResponse)
def show_quiz_get(request: Request):
    pass