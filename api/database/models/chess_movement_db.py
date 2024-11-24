"""chess movement data base"""

from sqlmodel import Field, SQLModel

class Chess_movement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="chess_game.id", index=True)
    index: int = Field(index=True)
    encoded_movement: int = Field(index= True)

