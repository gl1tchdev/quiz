from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from dependencies import get_db
from db.schemas import QuizCreate, QuestionCreate, AnswerCreate
from tools import *
from json import dumps

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
    quiz_list: List[models.Quiz] = get_quiz_list(db)
    if len(quiz_list) != 0:
        context.update({'quiz_list': quiz_list})
    return get_template("lobby.html", context)


@quiz.post('/search', response_class=HTMLResponse)
async def search(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    context.update({'user': user})
    form = await form_to_obj(request)
    query = form['query']
    quiz_items = get_quiz_list(db)
    sorted_quiz_items = intelligent_search(query, quiz_items)
    context.update({'quiz_list': sorted_quiz_items})
    context.update({'page_title': f'Searching: {query}'})
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
        response = RedirectResponse(request.url_for('create_question_form'))
        response.set_cookie(key='quiz_id', value=db_quiz.id)
        return response
    except ValidationError as exc:
        context.update({'errors': [loc_by_exception(error) for error in exc.errors()]})
        context.update(**form)
    context.update({'page_title': 'Create quiz'})
    return get_template("create_quiz.html", context)


@quiz.post('/create/questions', response_class=HTMLResponse)
async def create_question_form(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for("lobby_get"))
    form = await form_to_obj(request)
    quiz_id = request.cookies.get('quiz_id')
    if not quiz_id:
        return back
    quiz_id = int(quiz_id)
    context = prepare_context(request)
    quiz = get_quiz_by_id(db, quiz_id)
    if not quiz:
        return back
    questions = get_questions_by_quiz_id(db, quiz_id)
    if len(questions) == 5:
        return back
    checked = form_has_key('check', form)
    answered = form_has_key('answer', form)
    if answered and checked:
        form_dict = question_form_to_dict(form)
        question_text = form_dict[0]
        question_schema = QuestionCreate(text=question_text,
                                         quiz_id=quiz_id)
        db_question = create_question(db, question_schema, quiz_id)
        answers_dict = form_dict[1]
        answers = []
        for answer in answers_dict:
            answer_schema = AnswerCreate(text=answer['text'],
                                         question_id=db_question.id,
                                         is_correct=answer['is_correct'])
            answers.append(answer_schema)
        db_answers = create_answers(db, answers, db_question.id)
        context.update({"success": True})
    elif answered and not checked:
        context.update({"error": True})
    else:
        pass
    context.update({'quiz_id': quiz_id})
    questions = get_questions_by_quiz_id(db, quiz_id)
    question_len = len(questions)
    if question_len == 5:
        response = RedirectResponse(request.url_for('lobby_get').include_query_params(created=True))
        response.delete_cookie(key='quiz_id')
        return response
    else:
        context.update({'count': len(questions)})
    context.update({'page_title': 'Create question'})
    return get_template("create_question.html", context)


@quiz.get('/show', response_class=HTMLResponse)
async def show_quiz_get(request: Request, db: Session = Depends(get_db)):
    back = RedirectResponse(request.url_for('lobby_get'))
    cookie = request.cookies.get('hash')
    user = get_user_by_hash(db, cookie)
    quiz_id = request.query_params.get('quiz_id')
    if not quiz_id:
        return back
    quiz_id = int(quiz_id)
    quiz: models.Quiz = get_quiz_by_id(db, quiz_id)
    if not quiz:
        return back
    context = prepare_context(request)
    author = get_user(db, quiz.author_id)
    context.update({'quiz': quiz})
    context.update({'author': author})
    context.update({'session_id': generate_session_id()})
    context.update({'user': user})
    context.update({'page_title': quiz.title})
    response = get_template("show_quiz.html", context)
    response = delete_quiz_info(response)
    return response


@quiz.post('/show', response_class=HTMLResponse)
async def show_questions(request: Request, db: Session = Depends(get_db)):
    quiz_id = request.cookies.get('quiz_id')
    quiz_id = int(quiz_id)
    current_question = request.cookies.get('current_question')
    current_question = int(current_question)
    context = prepare_context(request)
    questions = get_questions_by_quiz_id(db, quiz_id)
    question = questions[current_question - 1]
    context.update({'question': question})
    answers = get_answers_by_question_id(db, question.id)
    context.update({'answers': answers})
    context.update({'current_question': current_question})
    context.update({'page_title': f'Question {current_question}'})
    response = get_template('show_questions.html', context)
    return response


@quiz.post('/show/start', response_class=HTMLResponse)
async def start_quiz(request: Request):
    form = await form_to_obj(request)
    response = RedirectResponse(request.url_for('show_questions'))
    response.set_cookie(key='quiz_id', value=form['quiz_id'])
    response.set_cookie(key='current_question', value=form['current_question'])
    response.set_cookie(key='session_id', value=form['session_id'])
    return response


@quiz.post('/show/process', response_class=HTMLResponse)
async def process(request: Request, db: Session = Depends(get_db)):
    form = await form_to_obj(request)
    question_id = form['question_id']
    response = RedirectResponse(request.url_for('show_questions'))
    if not form_has_key('check', form):
        return response
    quiz_id = request.cookies.get('quiz_id')
    quiz_id = int(quiz_id)
    current_question = request.cookies.get('current_question')
    session_id = request.cookies.get('session_id')
    current_question = int(current_question)
    current_question += 1
    user = get_user_by_hash(db, request.cookies.get('hash'))
    marked = get_answers_ids(form)
    marked = dumps(marked)
    try:
        marked = schemas.MarkedBase(quiz_id=quiz_id, user_id=user.id, question_id=question_id, session_id=session_id,
                                    marked=marked)
        create_marked(db, marked)
    except ValidationError:
        return response
    if current_question > 5:
        return RedirectResponse(request.url_for('show_final'))
    response.set_cookie(key='current_question', value=str(current_question))
    return response


@quiz.post('/final', response_class=HTMLResponse)
async def show_final(request: Request, db: Session = Depends(get_db)):
    context = prepare_context(request)
    cookie = request.cookies.get('hash')
    quiz_id = request.cookies.get('quiz_id')
    quiz_id = int(quiz_id)
    user: models.User = get_user_by_hash(db, cookie)
    context.update({'user': user})
    session_id = request.cookies.get('session_id')
    user_marked: List[models.Session] = get_session_info(db, session_id)
    output = process_quiz(db, user_marked, user)
    context.update({'results': output})
    context.update({'page_title': 'Quiz results'})
    context.update({'user': user})
    response = get_template("show_final.html", context)
    response = delete_quiz_info(response)
    return response


@quiz.post('/delete', response_class=HTMLResponse)
async def delete_q(request: Request, db: Session = Depends(get_db)):
    form = await form_to_obj(request)
    if form['user_id'] == form['author_id']:
        delete_quiz(db, int(form['quiz_id']))
    return RedirectResponse(request.url_for('lobby_get'))
