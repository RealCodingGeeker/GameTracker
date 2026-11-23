from typing import Optional
from sqlmodel import SQLModel, Field

class GameBase(SQLModel):
    title: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    hours_played: float = Field(default=0, ge=0)
    completed: bool = False

class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int

class GameUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1)
    platform: Optional[str] = Field(default=None, min_length=1)
    hours_played: Optional[float] = Field(default=None, ge=0)
    completed: Optional[bool] = None