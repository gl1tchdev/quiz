from pydantic import (BaseModel,
                      constr,
                      model_validator, Json)
from typing import Optional


from dependencies import get_db


class UserBase(BaseModel):
    login: constr(min_length=3, max_length=8, to_lower=True)


class UserCreate(UserBase):
    password: constr(min_length=5, max_length=15, to_lower=True)
    password2: str

    @model_validator(mode='after')
    def login_equals(self) -> 'UserCreate':
        if self.login == self.password:
            raise ValueError('login')
        return self

    @model_validator(mode='after')
    def passwords_equals(self) -> 'UserCreate':
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('password2')
        return self


class UserLogin(BaseModel):
    login: str
    password: str


class User(UserBase):
    id: int
    points: int

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    title: str
    description: Optional[str]
    author_id: int

    @model_validator(mode='after')
    def title_is_unique(self) -> 'QuizCreate':
        from db.crud import get_quiz_by_title
        db = next(get_db())
        quiz = get_quiz_by_title(db, self.title)
        if quiz:
            raise ValueError('title')
        return self


class QuestionCreate(BaseModel):
    text: str
    quiz_id: int


class AnswerCreate(BaseModel):
    text: str
    question_id: int
    is_correct: bool


class MarkedBase(BaseModel):
    quiz_id: int
    user_id: int
    question_id: int
    session_id: str
    marked: Json