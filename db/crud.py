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


def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(title=quiz.title, description=quiz.description, author_id=quiz.author_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz
