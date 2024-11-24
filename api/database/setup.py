"""setup the database on app initialization"""

from sqlmodel import Session, SQLModel, create_engine

import os

# ensure all models are defined before database setup
# pylint: disable=wildcard-import


#from models import *

# Define directamente la URL para SQLite
database_url = "sqlite:///C:/Users/ANGEL GABRIEL/OneDrive/Escritorio/TEC trabajos/Semestre 3/Parcial 3/IOT/Chess_pruebas/api_8/api/database/databaseChess.db"

#DATABASE_URL_VAR = "ECHO_CHESS_DB_URL"
#database_url = os.getenv(DATABASE_URL_VAR)

# Configuración específica para SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(database_url, connect_args=connect_args)


def setup_database() -> None:
    """setup the database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """yields a session from the ORM engine"""
    with Session(engine) as session:
        yield session
