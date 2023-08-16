import string
from random import choice
from db.models import Question
from typing import List
from fastapi import Request, Response
from pydantic import ValidationError
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

prepare_context = lambda request=None, empty=False: {'request': request} if not empty else {}
templates = Jinja2Templates('templates')
get_template = lambda name, context:  templates.TemplateResponse(name, context)


async def form_to_obj(request: Request):
    form = await request.form()
    return jsonable_encoder(form)


def loc_by_exception(error: ValidationError):
    return error['loc'][0] if error['type'].startswith('string') else error['msg'].replace('Value error, ', '')


# worst algo
def question_form_to_dict(form: dict):
    question = form.pop('question')
    answers = []
    for key in form:
        if 'check' in key:
            continue
        num = key.replace('answer', '')
        index = int(num)
        answers.append({
            'answer_id': index,
            'text': '',
            'is_correct': False
        })
    for form_key, form_value in form.items():
        num = form_key.replace('check', '').replace('answer', '')
        index = int(num)
        for answer in answers:
            if index == answer['answer_id']:
                if 'check' in form_key:
                    answer['is_correct'] = True
                else:
                    answer['text'] = form_value
    return [question, answers]


form_has_key = lambda word, form: any(word in key for key in form.keys())


def generate_session_id():
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(choice(letters) for _ in range(6))
    return result_str


def delete_quiz_info(response: Response):
    response.delete_cookie(key='current_question')
    response.delete_cookie(key='quiz_id')
    response.delete_cookie(key='session_id')
    return response


def get_answers_ids(form: dict):
    result = []
    for key, _ in form.items():
        if 'check' not in key:
            continue
        num = key.replace('check', '')
        index = int(num)
        result.append(index)
    return result

