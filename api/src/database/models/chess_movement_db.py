"""chess movement data base"""

from sqlmodel import Field, SQLModel

class ChessMovement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="chessgame.id", index=True)
    index: int = Field(index=True)
    encoded_movement: int = Field(index= True)

