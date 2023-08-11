from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

prepare_context = lambda request=None, empty=False: {'request': request} if not empty else {}
templates = Jinja2Templates('templates')
get_template = lambda name, context: templates.TemplateResponse(name, context)


async def form_to_obj(request):
    form = await request.form()
    return jsonable_encoder(form)


def loc_by_exception(error):
    return error['loc'][0] if error['type'].startswith('string') else error['msg'].replace('Value error, ', '')


# worst algo
def question_form_to_dict(form):
    question = form.pop('question')
    answers = []
    for key in form:
        if 'check' in key:
            continue
        index = int(key[-1])
        answers.append({
            'answer_id': index,
            'text': '',
            'is_correct': False
        })
    for form_key, form_value in form.items():
        index = int(form_key[-1])
        for answer in answers:
            if index == answer['answer_id']:
                if 'check' in form_key:
                    answer['is_correct'] = True
                else:
                    answer['text'] = form_value
    return [question, answers]
