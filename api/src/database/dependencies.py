"""FastAPI database dependencies declarations"""

from fastapi import Depends

from database.setup import get_session

DBSessionDependency = Depends(get_session)
