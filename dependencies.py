from sqlalchemy.orm import sessionmaker

from database.connection import db

SessionLocal = sessionmaker(bind=db)


def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
