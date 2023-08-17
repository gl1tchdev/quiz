from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    points = Column(Integer)
    hashed_password = Column(String)


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, unique=True)
    description = Column(String)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    question_id = Column(String, ForeignKey('questions.id'))
    is_correct = Column(Boolean)


class Session(Base):
    __tablename__ = 'answered'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    session_id = Column(String)
    marked = Column(JSON)
