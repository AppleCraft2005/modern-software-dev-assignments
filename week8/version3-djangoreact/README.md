# Task Manager v3 — Django REST Framework + React

A full-stack task manager with a Django REST API backend and a React (Vite + Tailwind CSS) frontend.

## Project Structure

```
version3-djangoreact/
├── backend/          # Django REST Framework API
│   ├── taskmanager/  # Django project settings & URLs
│   ├── tasks/        # Tasks app (model, serializer, viewset)
│   ├── manage.py
│   └── requirements.txt
├── frontend/         # React app (Vite)
│   ├── src/
│   │   ├── App.jsx   # Main UI with CRUD operations
│   │   ├── main.jsx  # React entry point
│   │   └── index.css # Tailwind CSS imports
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

---

## Backend Setup (Django)

1. **Open a terminal and navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/api/tasks/`.

---

## Frontend Setup (React)

1. **Open a new terminal and navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`.  
   API requests are proxied to the Django backend automatically via Vite's dev server proxy.

---

## API Endpoints

| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| GET    | `/api/tasks/`        | List all tasks      |
| POST   | `/api/tasks/`        | Create a new task   |
| GET    | `/api/tasks/{id}/`   | Retrieve a task     |
| PUT    | `/api/tasks/{id}/`   | Update a task       |
| PATCH  | `/api/tasks/{id}/`   | Partial update      |
| DELETE | `/api/tasks/{id}/`   | Delete a task       |

## Features

- Create, read, update, and delete tasks
- Toggle task completion status
- Inline editing of task title and description
- Clean, responsive UI with Tailwind CSS
