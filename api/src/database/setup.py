"""setup the database on app initialization"""

import os

from sqlmodel import Session, SQLModel, create_engine

# ensure all models are defined before database setup
# pylint: disable=wildcard-import
from database.models import *

DATABASE_URL_VAR = "ECHO_CHESS_DB_URL"

database_url = os.getenv(DATABASE_URL_VAR)

connect_args = {"check_same_thread": False}
engine = create_engine(database_url, connect_args=connect_args)


def setup_database() -> None:
    """setup the database and tables"""

    SQLModel.metadata.create_all(engine)


def get_session():
    """yields a session from the ORM engine"""

    with Session(engine) as session:
        yield session
