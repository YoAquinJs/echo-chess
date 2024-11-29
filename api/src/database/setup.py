"""setup the database on app initialization"""

import os

from sqlmodel import Session, SQLModel, create_engine

# ensure all models are defined before database setup
from database import models as _

DATABASE_URL_ENV = "ECHO_CHESS_DB_URL"
DATABASE_URL = os.environ.get(DATABASE_URL_ENV, None)

if DATABASE_URL is None:
    raise RuntimeError(f"missing {DATABASE_URL_ENV}")

# Configuración específica para SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def setup_database() -> None:
    """setup the database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """yields a session from the ORM engine"""
    with Session(engine) as session:
        yield session
