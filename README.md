# Task Manager

A Django-based task management application that helps users organize and track their tasks with features like categories, priorities, and due dates.

## Features

- User authentication (signup, login, logout)
- Dashboard with task statistics and overview
- Task management:
  - Create, edit, and delete tasks
  - Set task priorities (High, Medium, Low)
  - Add due dates
  - Mark tasks as completed
  - Categorize tasks
- Category management:
  - Create, edit, and delete categories
  - View tasks by category
- Task filtering and search:
  - Filter by status (completed/pending)
  - Filter by priority
  - Filter by category
  - Search tasks by title or description

## Technologies Used

- Python 3.12
- Django 5.2
- Bootstrap 5.3
- Font Awesome 6.0
- SQLite3

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/task_manager.git
cd task_manager
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install django
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser (admin):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

1. Register a new account or login with existing credentials
2. Create categories to organize your tasks
3. Add tasks with title, description, due date, priority, and category
4. View all tasks on the dashboard or task list
5. Filter and search tasks as needed
6. Mark tasks as completed when done
7. Manage categories and tasks through the intuitive interface

## Project Structure

- `tasks/`: Main application directory
  - `models.py`: Database models (Task, Category)
  - `views.py`: View functions and logic
  - `forms.py`: Form definitions
  - `urls.py`: URL routing
  - `templates/tasks/`: HTML templates
- `task_manager/`: Project settings directory
