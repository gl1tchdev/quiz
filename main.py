from fastapi import FastAPI
from quiz.routes import router
from fastapi.staticfiles import StaticFiles

def create_app():
    app = FastAPI()
    router.mount("/static", StaticFiles(directory="quiz/static"), name="static")
    app.include_router(router)
    return app

app = create_app()
