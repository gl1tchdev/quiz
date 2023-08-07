from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi import Cookie, Request
from fastapi.responses import RedirectResponse
from typing import Annotated, Union

prepare_context = lambda request=None, empty=False: {'request': request} if not empty else {}
templates = Jinja2Templates('templates')
get_template = lambda name, context: templates.TemplateResponse(name, context)


async def form_to_obj(request):
    result = await request.form()
    return jsonable_encoder(result)


def loc_by_exception(error):
    return error['loc'][0] if error['type'].startswith('string') else error['msg'].replace('Value error, ', '')

