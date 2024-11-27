"""board client data base"""

from sqlmodel import Field, SQLModel

class BoardClient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str | None = Field(index=True)
