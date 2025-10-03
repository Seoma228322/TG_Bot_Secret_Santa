from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from bot.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        return db
    finally:
        pass
