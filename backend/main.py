from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Game, GameCreate, GameRead, GameUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# CREATE
@app.post("/games", response_model=GameRead, status_code=201)
def create_game(game: GameCreate, session: Session = Depends(get_session)):
    db_game = Game.model_validate(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


# READ ALL
@app.get("/games", response_model=list[GameRead])
def read_games(session: Session = Depends(get_session)):
    return session.exec(select(Game)).all()


# READ ONE
@app.get("/games/{game_id}", response_model=GameRead)
def read_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


# UPDATE
@app.patch("/games/{game_id}", response_model=GameRead)
def update_game(game_id: int, updates: GameUpdate, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game.sqlmodel_update(updates.model_dump(exclude_unset=True))
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


# DELETE
@app.delete("/games/{game_id}")
def delete_game(game_id: int, session: Session = Depends(get_session)):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    session.delete(game)
    session.commit()
    return {"ok": True}