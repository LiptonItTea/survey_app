from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, VARCHAR, BIGINT
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user_accs"
    
    id = Column(Integer, nullable=False, primary_key=True)
    nickname = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=True)
    registration_date = Column(DateTime, nullable=False, default=datetime.now())
    hashed_password = Column(VARCHAR(255), nullable=False)
    

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"