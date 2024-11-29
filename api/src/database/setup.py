"""setup the database on app initialization"""

from sqlmodel import Session, SQLModel, create_engine

# ensure all models are defined before database setup
# pylint: disable=wildcard-import


#from models import *

# Define directamente la URL para SQLite
#Angel: no he entendido como hacer el direccionamiento de la base de datos
#con el otro método, quisiera pedirte ayuda con él
database_url = "sqlite:///database/databaseChess.db"

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
