# Game Tracker: Full-Stack CRUD Application

A FastAPI backend and Flask frontend for managing a collection of video games.

## Tech Stack
- **Backend:** FastAPI, SQLModel, SQLite
- **Frontend:** Flask with Jinja templates
- **Tests:** pytest

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run
Open two terminals (venv activated in both).

**API (port 8000):**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend (port 5000):**
```bash
cd frontend
python app.py
```

Then open http://127.0.0.1:5000. API docs are at http://127.0.0.1:8000/docs.

## Run Tests
```bash
cd backend
pytest -v
```

## API Endpoints
| Method | Path | Description |
|---|---|---|
| POST | /games | Create a game |
| GET | /games | Read all games |
| GET | /games/{id} | Read one game |
| PATCH | /games/{id} | Update a game |
| DELETE | /games/{id} | Delete a game |