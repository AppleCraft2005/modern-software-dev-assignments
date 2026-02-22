# Action Item Extractor

A FastAPI-based web application that converts free-form notes into actionable items, leveraging both heuristic extraction and LLM-powered intelligence to identify and organize tasks.

## Overview

The Action Item Extractor is a full-stack application built with:

- **Backend**: FastAPI with SQLite database for persistent storage
- **Frontend**: Minimal vanilla HTML/CSS/JavaScript interface
- **Extraction Engine**: Dual-mode action item extraction:
  - **Heuristic Mode**: Pattern-based extraction using bullet points, keyword prefixes, and imperative detection
  - **LLM Mode**: AI-powered extraction via Ollama for more intelligent task identification

### Key Features

**Multiple Extraction Methods**
- Heuristic extractor for fast, pattern-based action item identification
- LLM-powered extractor using Ollama for context-aware task extraction
- Fallback mechanism: LLM mode automatically reverts to heuristic if Ollama is unavailable

**Note Management**
- Create and store notes with automatic timestamps
- Link action items to parent notes for context
- List all notes with their associated metadata

**Task Tracking**
- Mark action items as complete/incomplete
- Persistent checkbox state in the web UI
- Associate items with source notes for traceability

**Clean Architecture**
- Pydantic schemas for strict API contracts
- Type-safe database layer with dictionary returns
- Centralized error handling with JSON responses
- Modular router design separating concerns

---

## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **Poetry** (for dependency management)
- **Ollama** (optional, for LLM-powered extraction)
- A compatible conda environment (e.g., `cs146s`)

### Step 1: Activate Environment

Activate your conda environment:

```bash
conda activate cs146s
```

### Step 2: Install Dependencies

From the project root, install dependencies using Poetry:

```bash
poetry install
```

### Step 3: (Optional) Set Up Ollama

If you want to use the LLM-powered extraction feature:

1. Download and install Ollama from [ollama.com](https://ollama.com)
2. Pull a model (e.g., `llama3.1:8b`):
   ```bash
   ollama pull llama3.1:8b
   ```
3. Start the Ollama server:
   ```bash
   ollama serve
   ```

   The app will gracefully fall back to heuristic extraction if Ollama is unavailable.

### Step 4: Run the Server

Start the FastAPI development server from the project root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

The server will initialize the SQLite database on startup at `week2/data/app.db`.

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

---

## API Endpoints and Functionality

### Notes Endpoints

#### Create a Note
```http
POST /notes
Content-Type: application/json

{
  "content": "Your note content here"
}
```

**Response (201 Created)**:
```json
{
  "id": 1,
  "content": "Your note content here",
  "created_at": "2026-02-22 12:34:56"
}
```

**Error Responses**:
- `400 Bad Request`: Missing or empty `content` field
- `500 Internal Server Error`: Database error

---

#### Get a Single Note
```http
GET /notes/{note_id}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "content": "Your note content",
  "created_at": "2026-02-22 12:34:56"
}
```

**Error Responses**:
- `404 Not Found`: Note does not exist
- `500 Internal Server Error`: Database error

---

#### List All Notes
```http
GET /notes/
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "content": "First note",
    "created_at": "2026-02-22 12:34:56"
  },
  {
    "id": 2,
    "content": "Second note",
    "created_at": "2026-02-22 12:45:00"
  }
]
```

---

### Action Items Endpoints

#### Extract Action Items (Heuristic)
```http
POST /action-items/extract
Content-Type: application/json

{
  "text": "- Set up database\n- Implement API\naction: Write tests",
  "save_note": true
}
```

**Request Fields**:
- `text` (string, required): The input text to extract action items from
- `save_note` (boolean, optional, default: false): Whether to save the input text as a note

**Response (200 OK)**:
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Set up database"
    },
    {
      "id": 2,
      "text": "Implement API"
    },
    {
      "id": 3,
      "text": "Write tests"
    }
  ]
}
```

**Error Responses**:
- `400 Bad Request`: Missing or empty `text` field
- `500 Internal Server Error`: Extraction or database error

**Extraction Patterns**:
- Bullet points: `- Item`, `* Item`, `• Item`
- Numbered lists: `1. Item`, `2. Item`
- Keyword prefixes: `todo:`, `action:`, `next:`
- Checkboxes: `[ ] Item`, `[todo] Item`
- Imperative sentences: Auto-detects sentences starting with verbs (add, create, implement, fix, update, write, check, verify, refactor, document, design, investigate)

---

#### Extract Action Items (LLM-Powered)
```http
POST /action-items/extract-llm
Content-Type: application/json

{
  "text": "During the meeting we discussed setting up the database and implementing the API. Next, we need to write comprehensive tests and deploy to production.",
  "save_note": true
}
```

**Request Fields**: (Same as heuristic extraction)
- `text` (string, required): The input text to extract action items from
- `save_note` (boolean, optional, default: false): Whether to save the input text as a note

**Response (200 OK)**: (Same structure as heuristic extraction)

**Benefits**:
- Understands context and natural language
- Extracts tasks from narrative text without explicit markers
- More intelligent grouping and deduplication

**Fallback Behavior**:
- If Ollama is unavailable, automatically falls back to heuristic extraction
- If JSON parsing fails, reverts to heuristic extraction

---

#### List All Action Items
```http
GET /action-items/
```

**Query Parameters** (optional):
- `note_id` (integer): Filter items by parent note ID

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "note_id": 1,
    "text": "Set up database",
    "done": false,
    "created_at": "2026-02-22 12:34:56"
  },
  {
    "id": 2,
    "note_id": 1,
    "text": "Implement API",
    "done": true,
    "created_at": "2026-02-22 12:35:00"
  }
]
```

---

#### Mark Action Item as Complete
```http
POST /action-items/{action_item_id}/done
Content-Type: application/json

{
  "done": true
}
```

**Request Fields**:
- `done` (boolean, optional, default: true): Whether to mark the item as complete

**Response (200 OK)**:
```json
{
  "id": 1,
  "note_id": 1,
  "text": "Set up database",
  "done": true,
  "created_at": "2026-02-22 12:34:56"
}
```

**Error Responses**:
- `404 Not Found`: Action item does not exist
- `500 Internal Server Error`: Database error

---

### Root Endpoint

#### Get the Web UI
```http
GET /
```

**Response**: HTML document containing the interactive frontend

---

## Frontend Usage

### Interface Overview

The web interface provides three main buttons for interaction:

#### Extract (Heuristic)
1. Paste or type your notes in the textarea
2. (Optional) Check the "Save as note" checkbox
3. Click **Extract** button
4. Action items appear as a checklist below

**Best for**: Structured notes with bullets, numbered lists, or keyword prefixes

#### Extract LLM
1. Paste or type your notes in the textarea
2. (Optional) Check the "Save as note" checkbox
3. Click **Extract LLM** button
4. Wait for the LLM to process (slower but more intelligent)
5. Action items appear as a checklist below

**Best for**: Natural language notes without explicit markers

#### List Notes
1. Click **List Notes** button
2. All saved notes display with their ID, content, and creation timestamp
3. Each note is shown in a styled card

### Marking Items Complete

- Click the checkbox next to any action item to mark it as complete
- Changes are saved immediately to the database
- The checkbox state persists across page reloads

---

## Testing

### Running the Test Suite

From the project root, run pytest:

```bash
pytest week2/tests/
```

To run tests with verbose output:

```bash
pytest week2/tests/ -v
```

To run a specific test file:

```bash
pytest week2/tests/test_extract.py -v
```

### Test Coverage

#### Heuristic Extraction Tests (`test_extract.py`)
- **test_extract_bullets_and_checkboxes**: Validates extraction of bullet points, numbered lists, and checkboxes
- Includes assertions for correct parsing of multiple list formats

#### LLM-Powered Extraction Tests (`test_extract.py`)
- **test_extract_action_items_llm_with_bulleted_list**: Mocks the Ollama chat function and validates normal bulleted list extraction
- **test_extract_action_items_llm_with_empty_input**: Ensures graceful handling of empty input strings
- **test_extract_action_items_llm_with_keyword_prefixes**: Validates extraction from keyword-prefixed lines

**Test Approach**:
- Uses `pytest` and `pytest-asyncio` for async test execution
- Mocks the Ollama chat function with `unittest.mock.AsyncMock` to avoid external LLM calls during testing
- Fixtures return properly formatted JSON strings matching the expected response format

### Running Tests with Coverage

To see code coverage:

```bash
pytest week2/tests/ --cov=week2.app --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`

---

## Project Structure

```
week2/
├── README.md                # This file
├── assignment.md            # Assignment specification
├── writeup.md              # Implementation writeup
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app initialization and global error handlers
│   ├── db.py               # SQLite database operations and schema
│   ├── schemas.py          # Pydantic models for API contracts
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── notes.py        # Note CRUD endpoints
│   │   └── action_items.py # Action item endpoints (both heuristic and LLM)
│   └── services/
│       └── extract.py      # Extraction logic (heuristic and LLM)
├── data/
│   └── app.db              # SQLite database (auto-created on startup)
├── frontend/
│   └── index.html          # Web UI with three interactive buttons
└── tests/
    ├── __init__.py
    └── test_extract.py     # Unit tests for extraction functions
```

---

## Database Schema

### Notes Table
```sql
CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);
```

### Action Items Table
```sql
CREATE TABLE action_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  note_id INTEGER,
  text TEXT NOT NULL,
  done INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (note_id) REFERENCES notes(id)
);
```

---

## Architecture Decisions

### Pydantic Schemas
All API requests and responses are validated using Pydantic models:
- `NoteCreate`: Input validation for note creation
- `NoteRead`: Output schema for note retrieval
- `ActionItemCreate`: Input validation for action item creation
- `ActionItemRead`: Output schema for action item retrieval

**Benefits**:
- Type safety and automatic validation
- Auto-generated OpenAPI documentation
- Clear API contracts

### Database Layer
- Functions return dictionaries instead of raw SQLite Row objects
- `_row_to_dict()` helper for consistent type conversion
- All database operations are type-hinted for clarity

### Error Handling
- Global exception handlers return consistent JSON error responses
- `RequestValidationError` returns detailed validation error info (422)
- Generic exceptions return user-friendly error messages (500)

### Extraction Fallback
- LLM extractor gracefully falls back to heuristic mode if:
  - Ollama is not installed or unreachable
  - Chat function is not available
  - JSON parsing fails
  - Any LLM-related error occurs

---

## Troubleshooting

### "Connection refused" when running LLM extraction
**Solution**: Ensure Ollama is running (`ollama serve` in another terminal) or rely on the fallback heuristic extractor.

### "No module named 'ollama'"
**Solution**: The app will gracefully use heuristic extraction. Install ollama-python if you want LLM support: `pip install ollama`

### Database locked error
**Solution**: Ensure no other instances of the app are running. The SQLite database in `week2/data/app.db` is locked when in use.

### Empty extraction results
**Solution**:
- **Heuristic mode**: Check that your input uses recognized patterns (bullets, keywords, checkboxes, or imperative verbs)
- **LLM mode**: Provide more context or rephrase using natural language

### Port 8000 already in use
**Solution**: Run on a different port:
```bash
poetry run uvicorn week2.app.main:app --reload --port 8001
```

---

## Dependencies

Key dependencies (managed by Poetry):

- **fastapi**: Modern Python web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation using Python type annotations
- **sqlite3**: Built-in database (no external dependency needed)
- **ollama**: (Optional) LLM inference client for structured outputs
- **pytest**: Testing framework
- **pytest-asyncio**: async/await support for pytest

---

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Database migration system (Alembic)
- [ ] Advanced filtering and sorting on list endpoints
- [ ] Batch action item operations
- [ ] Support for multiple extraction models
- [ ] Action item categorization and tagging
- [ ] Export functionality (CSV, JSON)
- [ ] Webhook support for external integrations

---

## Contributing

When adding new features:

1. Update schemas in `schemas.py` for new request/response types
2. Add database operations to `db.py` if needed
3. Create or update routers in `routers/`
4. Write unit tests covering edge cases
5. Update this README with new endpoint documentation

---

## License

This is an educational project for the Modern Software Development course.

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the assignment specification in `assignment.md`
3. Check the implementation writeup in `writeup.md`
