"""user data base"""

from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    password: str = Field(index= True)
    board_token: int | None = Field(index= True)

