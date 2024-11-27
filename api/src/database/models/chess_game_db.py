"""chess game data base"""

from sqlmodel import Field, SQLModel

class ChessGame(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    white_user_id: int = Field(foreign_key="user.id", index=True)
    black_user_id: int = Field(foreign_key="user.id", index=True)
    status: int = Field(index= True)
    
    