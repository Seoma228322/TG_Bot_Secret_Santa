from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
    hobbies = Column(String)
    is_admin = Column(Boolean, default=False)
    gift_sent = Column(Boolean, default=False)
    recipient_id = Column(Integer, nullable=True)
    