# To-Do API

A simple Django REST Framework API for managing to-do tasks.

## Installation

1. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Start development server**
```bash
python manage.py runserver
```

## Running Tests

```bash
python manage.py test todos.tests
```

## API Endpoints

Base URL: `http://localhost:8000/api`

### List All Tasks
```bash
curl http://localhost:8000/api/tasks/
```

### Create a Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "completed": false}'
```

### Update Task Title
```bash
curl -X PUT http://localhost:8000/api/tasks/1/title/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title"}'
```

### Toggle Task Completion
```bash
curl -X POST http://localhost:8000/api/tasks/1/toggle/
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/tasks/1/
```

## Quick Start

```bash
# Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Django", "completed": false}'

# List all tasks
curl http://localhost:8000/api/tasks/

# Mark task as completed
curl -X POST http://localhost:8000/api/tasks/1/toggle/

# Delete task
curl -X DELETE http://localhost:8000/api/tasks/1/
```

## License

This is a learning project for demonstration purposes.
