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


# {'check1': 'true', 'answer1': 'asd', 'answer2': 'asd'}
def process_form_to_dict(form):
    # TODO: think about data structures
    '''
    question = form.pop('question')
    answers = []
    for key in form:
        if 'check' in key:
            continue
        index = int(key[-1])
        answers.append({
            index: {
                'text': '',
                'is_correct': True
            }
        })
    for key, value in form.items():
        if 'check' in key:
            answers
    print(form)
    return [question, answers]
    '''
