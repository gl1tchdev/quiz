from fastapi.templating import Jinja2Templates

prepare_context = lambda request: {'request': request}
templates = Jinja2Templates('templates')
get_template = lambda name, context: templates.TemplateResponse(name, context)