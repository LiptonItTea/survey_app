from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, VARCHAR, BIGINT, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user_accs"
    
    id = Column(Integer, nullable=False, primary_key=True)
    nickname = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=True)
    registration_date = Column(DateTime, nullable=False, default=datetime.now())
    hashed_password = Column(VARCHAR(255), nullable=False)
    
    # Relationships
    created_surveys = relationship("Survey", back_populates="creator", cascade="all, delete-orphan")
    completed_surveys = relationship("CompletedSurvey", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
    

class Survey(Base):
    __tablename__ = "survey"
    
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(Text, nullable=True)
    id_user_creator = Column(Integer, ForeignKey("user_accs.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="created_surveys")
    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Survey id={self.id} name={self.name}>"
    

class Question(Base):
    __tablename__ = "question"
    
    id = Column(Integer, nullable=False, primary_key=True)
    text = Column(Text, nullable=True)
    multiple_answers = Column(Boolean, nullable=True, default=False)
    id_survey = Column(Integer, ForeignKey("survey.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    survey = relationship("Survey", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question id={self.id} text='{self.text[:30]}...'>"
    

class Answer(Base):
    __tablename__ = "answer"
    
    id = Column(Integer, nullable=False, primary_key=True)
    text = Column(Text, nullable=True)
    id_question = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    question_answers = relationship("QuestionAnswer", back_populates="answer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Answer id={self.id} text='{self.text[:30]}...'>"
    

class CompletedSurvey(Base):
    __tablename__ = "completed_survey"
    
    id = Column(Integer, nullable=False, primary_key=True)
    id_user = Column(Integer, ForeignKey("user_accs.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="completed_surveys")
    question_answers = relationship("QuestionAnswer", back_populates="completed_survey", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CompletedSurvey id={self.id} user_id={self.id_user}>"
    

class QuestionAnswer(Base):
    __tablename__ = "question_answer"
    
    id = Column(Integer, nullable=False, primary_key=True)
    id_completed_survey = Column(Integer, ForeignKey("completed_survey.id", ondelete="CASCADE"), nullable=False)
    id_answer = Column(Integer, ForeignKey("answer.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    completed_survey = relationship("CompletedSurvey", back_populates="question_answers")
    answer = relationship("Answer", back_populates="question_answers")

    def __repr__(self):
        return f"<QuestionAnswer id={self.id} completed_survey={self.id_completed_survey} answer_id={self.id_answer}>"