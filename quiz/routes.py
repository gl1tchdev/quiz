from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from tools import *

quiz = APIRouter(prefix='/quiz')


@quiz.post('/', response_class=HTMLResponse)
def lobby_post(request: Request):
    context = prepare_context(request)
    return get_template("lobby.html", context)


@quiz.get('/', response_class=HTMLResponse)
def lobby_get(request: Request):
    context = prepare_context(request)
    return get_template("lobby.html", context)
