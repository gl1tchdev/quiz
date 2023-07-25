from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



prepare_context = lambda request: {'request': request}
get_template = lambda name, context: templates.TemplateResponse(name, context)


templates = Jinja2Templates(directory="quiz/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = prepare_context(request)
    context.update({'message': 'hello world'})
    return get_template('login.html', context)
