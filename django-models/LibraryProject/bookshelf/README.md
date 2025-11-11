# 📚 LibraryProject - Django Introduction

A basic Django project created to learn Django fundamentals, including project setup, structure exploration, and development server usage.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Project Structure](#project-structure)
- [Running the Development Server](#running-the-development-server)
- [Key Components Explained](#key-components-explained)
- [Next Steps](#next-steps)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Repository Information](#repository-information)
- [Learning Resources](#learning-resources)
- [Summary](#summary)

## ⚙️ Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- pip (Python package installer)
- A code editor (VS Code, PyCharm, or similar)
- Basic command line knowledge

To verify Python installation:
```bash
python --version
# or
python3 --version
```

## 🚀 Installation Steps

### 1. Install Django

Open your terminal and install Django using pip:
```bash
pip install django
```

To verify the installation:
```bash
python -m django --version
```

### 2. Create the Django Project

Navigate to your desired directory and create the project:
```bash
# Navigate to your Alx_DjangoLearnLab repository
cd Alx_DjangoLearnLab/Introduction_to_Django

# Create the Django project
django-admin startproject LibraryProject
```

### 3. Navigate to Project Directory
```bash
cd LibraryProject
```

## 📁 Project Structure

After creating the project, you'll see the following structure:
```
LibraryProject/
├── manage.py
├── README.md
└── LibraryProject/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🌐 Running the Development Server

### Start the Server

From within the LibraryProject directory (where manage.py is located):
```bash
python manage.py runserver
```

You should see output similar to:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

November 03, 2025 - 12:00:00
Django version 5.0, using settings 'LibraryProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

You should see the Django welcome page with a rocket ship, confirming successful setup! 🚀

### Stop the Server

Press `CTRL+C` in the terminal to stop the development server.

## 🔧 Key Components Explained

### 1. `manage.py`
**Purpose**: Command-line utility for administrative tasks

**Common Commands**:
- `python manage.py runserver` - Start the development server
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create an admin user
- `python manage.py startapp <app_name>` - Create a new Django app

**Key Point**: You should never need to edit this file. It's your interface to interact with Django.

---

### 2. `settings.py`
**Purpose**: Central configuration file for your Django project

**Important Settings**:
- **DEBUG**: Set to `True` for development, `False` for production
- **ALLOWED_HOSTS**: List of host/domain names that this Django site can serve
- **INSTALLED_APPS**: List of all Django applications activated in this project
- **DATABASES**: Database configuration (default: SQLite)
- **STATIC_URL**: URL prefix for static files (CSS, JavaScript, images)
- **SECRET_KEY**: Used for cryptographic signing (keep this secret in production!)

**Example Configuration Sections**:
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

### 3. `urls.py`
**Purpose**: URL routing configuration - the "table of contents" for your site

**Function**: Maps URL patterns to views (the functions that handle requests)

**Default Structure**:
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

**How It Works**:
- When a user visits a URL, Django checks `urlpatterns` from top to bottom
- When it finds a match, Django calls the associated view function
- The view returns an HTTP response

**Example with Custom URLs**:
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # Include app-specific URLs
]
```

---

### 4. Other Important Files

**`__init__.py`**
- Empty file that tells Python this directory is a Python package

**`wsgi.py`**
- Entry point for WSGI-compatible web servers to serve your project
- Used in production deployments

**`asgi.py`**
- Entry point for ASGI-compatible web servers
- Enables async features and WebSocket support

## 📝 Next Steps

Now that you have a working Django project, consider:

1. **Apply Migrations**: Initialize the database
```bash
python manage.py migrate
```

2. **Create a Superuser**: Access the Django admin interface
```bash
python manage.py createsuperuser
```

3. **Create Your First App**: Django projects consist of apps
```bash
python manage.py startapp books
```

4. **Explore the Admin Interface**: Visit `http://127.0.0.1:8000/admin/`

5. **Learn About Models**: Define your data structure

6. **Create Views**: Handle user requests

7. **Design Templates**: Create HTML pages

## ❗ Common Issues and Solutions

### Port Already in Use
If port 8000 is busy, specify a different port:
```bash
python manage.py runserver 8080
```

### Module Not Found
Ensure Django is installed in your Python environment:
```bash
pip list | grep Django
```

### Permission Denied
On some systems, use `python3` instead of `python`:
```bash
python3 manage.py runserver
```

## 📂 Repository Information

- **GitHub Repository**: `Alx_DjangoLearnLab`
- **Directory**: `Introduction_to_Django`
- **Project**: `LibraryProject`

## 📚 Learning Resources

- [Official Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django for Beginners Book](https://djangoforbeginners.com/)

## ✨ Summary

You've successfully:
- ✅ Installed Django
- ✅ Created a Django project named LibraryProject
- ✅ Run the development server
- ✅ Explored the project structure
- ✅ Understood key components (settings.py, urls.py, manage.py)

**Congratulations on taking your first steps with Django!** 🎉

---

*Created as part of the ALX Django Learning Lab curriculum* 🎓