# Claude Guide for This Project

## Week 4 Application Structure
- This is a FastAPI backend application with a simple static frontend.
- **Backend:** Router code and main logic are located in the `week4/backend/app/` folder.
- **Database:** Uses SQLite with SQLAlchemy. The schema is located in `week4/backend/app/models.py`.
- **Frontend:** Static files (HTML/JS) are located in `week4/frontend/`.
- **Tests:** Tests using `pytest` are located in `week4/backend/tests/`.

## Coding Guidelines (Guardrails)
1. **Do Not Delete Data:** Never touch or modify the initial data in `week4/data/seed.sql` unless explicitly instructed.
2. **Standard Linting:** After making changes to Python files, you **must** format the code using `black` or `ruff` before letting me review it.
3. **Write Tests First:** If asked to add a new feature (e.g., a new API endpoint in the router), write the failing test first in the `tests/` folder, then create the implementation code.
4. **Run Command:** The application is run using the command `uvicorn backend.app.main:app --reload` (since the `make` command is not natively recognized on Windows).

## Communication Style
- Please explain briefly and in casual Indonesian.
- Tell me exactly which files you modified.