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
    db_user = models.User(login=user.login, hashed_password=hashed_password, points=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_quiz_list(db: Session, skip: int = 0, limit: int = 0):
    result = None
    if limit > 0:
        result = db.query(models.Quiz).offset(skip).limit(limit).all()
    else:
        result = db.query(models.Quiz).all()
    return result


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
    return db.query(models.Question).order_by(models.Question.id).filter(models.Question.quiz_id == quiz_id).all()


def get_question_by_id(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


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


def get_answers_by_question_id(db: Session, question_id: int):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()


def get_answers_by_ids(db: Session, ids: List[int]):
    return db.query(models.Answer).filter(models.Answer.id.in_(tuple(ids))).all()


def create_marked(db: Session, marked_schema: schemas.MarkedBase):
    db_marked = models.Session(quiz_id=marked_schema.quiz_id, user_id=marked_schema.user_id,
                               question_id=marked_schema.question_id, session_id=marked_schema.session_id,
                               marked=marked_schema.marked)
    db.add(db_marked)
    db.commit()
    db.refresh(db_marked)
    return db_marked


def get_session_info(db: Session, session: str):
    return db.query(models.Session).filter(models.Session.session_id == session).order_by(models.Session.id).all()


def increment_user_score(db: Session, user: models.User):
    score = user.points or 0
    score += 1
    user.points = score
    db.commit()
    db.refresh(user)
    return user


def delete_quiz(db: Session, quiz_id: int) -> None:
    questions: List[models.Question] = get_questions_by_quiz_id(db, quiz_id)
    for question in questions:
        answers: List[models.Answer] = get_answers_by_question_id(db, question.id)
        for answer in answers:
            db.query(models.Answer).filter(models.Answer.id == answer.id).delete()
        db.query(models.Question).filter(models.Question.id == question.id).delete()
    db.query(models.Quiz).filter(models.Quiz.id == quiz_id).delete()
    db.commit()