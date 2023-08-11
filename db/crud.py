from typing import List

from . import models, schemas
from sqlalchemy.orm import Session
from auth import password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_hash(db: Session, hash: str):
    return db.query(models.User).filter(models.User.hashed_password == hash).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = password.get_password_hash(user.password)
    db_user = models.User(login=user.login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_quiz_by_title(db: Session, title: str):
    return db.query(models.Quiz).filter(models.Quiz.title == title).first()


def get_quiz_by_id(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()


def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(title=quiz.title, description=quiz.description, author_id=quiz.author_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def get_questions_by_quiz_id(db: Session, quiz_id: int):
    return db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()


def create_question(db: Session, question: schemas.QuestionCreate, quiz_id: int):
    db_question = models.Question(text=question.text, quiz_id=quiz_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def create_answers(db: Session, answers: List[schemas.AnswerCreate], question_id: int):
    db_answers = []
    for answer in answers:
        db_answer = models.Answer(text=answer.text, question_id=question_id, is_correct=answer.is_correct)
        db_answers.append(db_answer)
        db.add(db_answer)
    db.commit()
    return db_answers