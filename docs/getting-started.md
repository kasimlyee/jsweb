# Getting Started with JsWeb

Welcome to JsWeb! This comprehensive guide will walk you through setting up your development environment, creating your first project, and running your application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Creating a New Project](#creating-a-new-project)
- [Understanding the Project Structure](#understanding-the-project-structure)
- [Running the Development Server](#running-the-development-server)
- [Next Steps](#next-steps)
- [Tips & Tricks](#tips--tricks)

## Prerequisites

Before you begin, ensure you have the following installed:

!!! note "System Requirements"
    - **Python 3.8+** (Python 3.10+ is recommended for best performance)
    - **pip** (Python package manager)
    - A terminal or command prompt
    - A text editor or IDE (VS Code, PyCharm, etc.)

## Installation

JsWeb is available on PyPI and can be installed with `pip`. We recommend using a virtual environment to manage your project's dependencies.

### Step 1: Create and Activate a Virtual Environment

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

!!! tip "Virtual Environments"
    Virtual environments isolate your project dependencies from your system Python. This is considered a best practice and prevents dependency conflicts.

### Step 2: Install JsWeb

```bash
pip install jsweb
```

Verify the installation:

```bash
jsweb --version
```

## Creating a New Project

Once JsWeb is installed, use the CLI to generate a new project with a standard structure and all necessary files.

```bash
jsweb new myproject
cd myproject
```

!!! info "Project Creation"
    The `jsweb new` command creates a production-ready project structure with all boilerplate code you need to start building.

## Understanding the Project Structure

After running `jsweb new myproject`, your project will look like this:

```
myproject/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   └── env.py
├── static/                     # Static files (CSS, JS, images)
│   └── global.css
├── templates/                  # HTML templates
│   ├── login.html
│   ├── profile.html
│   └── register.html
├── alembic.ini                # Alembic configuration
├── app.py                     # Main application file
├── auth.py                    # Authentication logic
├── config.py                  # Configuration settings
├── forms.py                   # Form definitions
├── models.py                  # Database models
└── views.py                   # Route handlers
```

### Key Files Explained

| File          | Purpose                                                    |
|---------------|-------------------------------------------------------------|
| `app.py`      | Creates and configures your JsWeb application instance     |
| `config.py`   | Stores application configuration (database, secret key, etc) |
| `models.py`   | Define your database models/tables                          |
| `views.py`    | Define your routes and request handlers                     |
| `forms.py`    | Define your HTML forms and validation rules                |
| `auth.py`     | Handle user authentication and authorization                |
| `templates/`  | Store your HTML templates                                  |
| `static/`     | Store CSS, JavaScript, and image files                      |

## Running the Development Server

To run your new JsWeb application:

```bash
jsweb run --reload
```

### Command Options

| Option | Description |
|--------|-------------|
| `--reload` | Auto-restart server when code changes (highly recommended) |
| `--host` | Host to run on (default: `127.0.0.1`) |
| `--port` | Port to run on (default: `8000`) |
| `--qr` | Display QR code for network access |

!!! success "Server Started"
    You should see output like `Application startup complete`. Your app is now running at **http://127.0.0.1:8000**

Visit `http://127.0.0.1:8000` in your browser to see your application in action!

## Next Steps

Now that you have a running JsWeb project, here are the topics you should explore:

1. **[Routing](routing.md)** - Learn how to define routes and handle different URLs
2. **[Templating](templating.md)** - Use Jinja2 templates to render dynamic HTML
3. **[Database](database.md)** - Set up models and manage your database
4. **[Forms](forms.md)** - Create forms with validation
5. **[Blueprints](blueprints.md)** - Organize your code into modules
6. **[Admin Interface](admin.md)** - Use the built-in admin panel
7. **[Configuration](configuration.md)** - Configure your application

## Tips & Tricks

!!! tip "Hot Reload During Development"
    Always use `jsweb run --reload` during development. This saves you from manually restarting the server every time you change code.

!!! tip "QR Code Access"
    Use `jsweb run --reload --qr` to generate a QR code for accessing your app from other devices on your network.

!!! warning "Production"
    The development server is not suitable for production. Use a proper ASGI server like Uvicorn, Gunicorn with an ASGI worker, or Daphne for production deployments.

!!! info "Database Setup"
    If you're using a database, run `jsweb db upgrade` to apply migrations before starting the server.

