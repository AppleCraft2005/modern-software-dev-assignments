# Task Manager — Version 2 (FastAPI + Vanilla JS + SQLite)

A simple CRUD task manager with a FastAPI backend, SQLite database, and a Tailwind CSS / Vanilla JS frontend.

## Prerequisites

- Python 3.10+

## Setup & Run

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:

   ```bash
   uvicorn main:app --reload
   ```

4. **Open the app** in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------------|---------------------|
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get a single task |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
