# 📚 LibraryProject — Django Introduction

A minimal, hands-on Django project used to learn core Django concepts: project setup, structure, and how to run the development server.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start (Windows / PowerShell)](#quick-start-windows--powershell)
- [Installation Steps](#installation-steps)
- [Project Structure](#project-structure)
- [Running the Development Server](#running-the-development-server)
- [Key Components Explained](#key-components-explained)
- [Next Steps](#next-steps)
- [Common Issues & Solutions](#common-issues--solutions)
- [Repository Information](#repository-information)
- [Learning Resources](#learning-resources)
- [Summary](#summary)

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A code editor (VS Code, PyCharm, etc.)
- Basic command-line knowledge

Verify Python from PowerShell:

```powershell
python --version
# or
python3 --version
```

It is recommended to use a virtual environment for development. Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
``` 

---

## Quick Start (Windows / PowerShell)

1. Open PowerShell and navigate to your learning folder:

```powershell
cd C:\Users\DELL\Alx_DjangoLearnLab\Introduction_to_Django
```

2. (Optional) Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Django:

```powershell
pip install django
```

4. Create the project (if not already created):

```powershell
django-admin startproject LibraryProject
cd LibraryProject
```

---

## Installation Steps

Install Django and confirm the version:

```powershell
pip install django
python -m django --version
```

Create the project (if you haven't already):

```powershell
django-admin startproject LibraryProject
cd LibraryProject
```

Apply initial migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

---

## Project Structure

Typical layout for this project:

```
LibraryProject/
├── manage.py
├── README.md
├── db.sqlite3
└── LibraryProject/
	├── __init__.py
	├── asgi.py
	├── settings.py
	├── urls.py
	├── wsgi.py
	└── __pycache__/
```

Files to know:
- `manage.py` — CLI entrypoint for Django management commands
- `settings.py` — central configuration (databases, apps, static files, etc.)
- `urls.py` — root URL routing
- `wsgi.py` / `asgi.py` — entrypoints for WSGI/ASGI servers

---

## Running the Development Server

From the project directory (where `manage.py` lives):

```powershell
python manage.py runserver
```

Expected output (example):

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have X unapplied migration(s). Run 'python manage.py migrate' to apply them.

Django version X.X, using settings 'LibraryProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Stop the server with CTRL+C in the terminal.

---

## Key Components Explained

- `manage.py` — Utility for administrative tasks (runserver, migrate, createsuperuser, startapp).
- `settings.py` — Configuration; important settings include `DEBUG`, `ALLOWED_HOSTS`, `INSTALLED_APPS`, `DATABASES`, `SECRET_KEY`.
- `urls.py` — URL routing table; includes `path()` and `include()` for app routes.
- `wsgi.py` / `asgi.py` — Production entrypoints for WSGI/ASGI servers.
- `__init__.py` — Indicates Python package.

Example `settings.py` snippets:

```python
# Security
SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

# Applications
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

# Database (default: SQLite)
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}
```

---

## Next Steps

1. Apply migrations:

```powershell
python manage.py migrate
```

2. Create an admin user:

```powershell
python manage.py createsuperuser
```

3. Create an app (example `books`):

```powershell
python manage.py startapp books
```

4. Explore models, views, templates, and the admin interface at `/admin/`.

---

## Common Issues & Solutions

- Port already in use: run server on a different port

```powershell
python manage.py runserver 8080
```

- Module not found / Django not installed: ensure the virtual environment is active and reinstall

```powershell
pip install django
```

- Permission issues on some systems: try `python3` if `python` is not available.

---

## Repository Information

- Repository: `Alx_DjangoLearnLab`
- Directory: `Introduction_to_Django/LibraryProject`

---

## Learning Resources

- Django docs: https://docs.djangoproject.com/
- Official tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Django for Beginners: https://djangoforbeginners.com/

---

## Summary

You now have a working Django project and know how to:

- Install Django
- Create a project
- Run the development server
- Apply migrations and create a superuser

Next recommended tasks: add an app (e.g., `books`), define models, and register models with the admin site.

---

*Created as part of the ALX Django Learning Lab curriculum*
