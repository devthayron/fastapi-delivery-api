from pwdlib import PasswordHash
from sqlalchemy.orm import sessionmaker

from database.connection import db

SessionLocal = sessionmaker(bind=db)

password_hasher = PasswordHash.recommended()


def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
