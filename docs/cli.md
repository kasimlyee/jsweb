# Command-Line Interface

JsWeb comes with a powerful command-line interface (CLI) that helps you manage your application. You can use it to create new projects, run the development server, manage database migrations, and more.

## Table of Contents

- [Available Commands](#available-commands)
- [jsweb run](#jsweb-run)
- [jsweb new](#jsweb-new)
- [jsweb db](#jsweb-db)
- [jsweb create-admin](#jsweb-create-admin)
- [Tips & Tricks](#tips--tricks)

## Available Commands

Here's a quick overview of all CLI commands:

| Command | Purpose |
|---------|---------|
| `jsweb run` | Start the development server |
| `jsweb new` | Create a new JsWeb project |
| `jsweb db prepare` | Generate a new migration |
| `jsweb db upgrade` | Apply migrations to database |
| `jsweb db downgrade` | Revert the last migration |
| `jsweb create-admin` | Create a new admin user |

## jsweb run

Starts the development server with optional configuration.

```bash
jsweb run
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | The host to bind to | `127.0.0.1` |
| `--port` | The port to listen on | `8000` |
| `--reload` | Enable auto-reloading on code changes | Disabled |
| `--qr` | Display QR code for network access | Disabled |

### Examples

```bash
# Basic server
jsweb run

# With auto-reload (recommended for development)
jsweb run --reload

# On different port
jsweb run --port 5000

# Accessible from other machines
jsweb run --host 0.0.0.0 --reload

# With QR code for mobile access
jsweb run --reload --qr

# All options combined
jsweb run --host 0.0.0.0 --port 3000 --reload --qr
```

!!! tip "Development"
    Always use `--reload` during development to automatically restart the server when you save changes.

!!! warning "Production"
    The development server is NOT suitable for production. Use a proper ASGI server like:
    - Uvicorn
    - Hypercorn
    - Daphne
    
    ```bash
    # Production example with Uvicorn
    pip install uvicorn
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

## jsweb new

Creates a new JsWeb project with a production-ready directory structure.

```bash
jsweb new my_project
```

### What Gets Created

```
my_project/
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── static/                     # Static files (CSS, JS, images)
│   └── global.css
├── templates/                  # HTML templates
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   └── starter_template.html
├── alembic.ini                # Alembic configuration
├── app.py                     # Main application
├── auth.py                    # Authentication
├── config.py                  # Configuration
├── forms.py                   # Form definitions
├── models.py                  # Database models
└── views.py                   # Route handlers
```

### Quick Start After Creating

```bash
cd my_project
pip install jsweb
jsweb run --reload
```

## jsweb db

Database management commands for migrations using Alembic.

### jsweb db prepare

Generate a new migration based on model changes.

```bash
jsweb db prepare -m "Create user table"
```

**Options:**

| Option | Description | Required |
|--------|-------------|----------|
| `-m`, `--message` | Description of the migration | Yes |

**Examples:**

```bash
# Simple migration
jsweb db prepare -m "Add email field to users"

# Detailed messages are helpful
jsweb db prepare -m "Create products table with inventory tracking"

# Structural changes
jsweb db prepare -m "Add foreign key relationships between posts and users"
```

!!! tip "Descriptive Messages"
    Use clear, descriptive messages that explain what the migration does. This helps when reviewing migration history.

### jsweb db upgrade

Apply all pending migrations to the database.

```bash
jsweb db upgrade
```

**When to use:**

- After creating a new project (to initialize database)
- After pulling code with new migrations
- Before deploying to production

**Examples:**

```bash
# Apply all pending migrations
jsweb db upgrade

# Deploy workflow
git pull
jsweb db upgrade
jsweb run --reload
```

!!! warning "Backup Before Upgrade"
    Always backup your database before running migrations in production!
    
    ```bash
    # SQLite backup
    cp app.db app.db.backup
    jsweb db upgrade
    ```

### jsweb db downgrade

Revert the last applied migration (one step back).

```bash
jsweb db downgrade
```

**Use cases:**

- Accidentally applied the wrong migration
- Need to test migration rollback
- Rolling back changes

**Examples:**

```bash
# Revert last migration
jsweb db downgrade

# Check status after downgrade
jsweb db upgrade  # See current migrations
```

!!! danger "Production Downgrades"
    Be very careful downgrading in production. Data loss may occur depending on the migration.

## jsweb create-admin

Create a new administrator user for the admin interface.

```bash
jsweb create-admin
```

### Interactive Prompts

The command will ask for:
1. **Username**: Unique admin username
2. **Email**: Admin email address
3. **Password**: Secure password (input hidden)

```bash
$ jsweb create-admin
Username: admin
Email: admin@example.com
Password: ••••••••
Password (confirm): ••••••••

Admin user 'admin' created successfully!
```

!!! tip "Multiple Admins"
    You can create multiple admin users by running this command multiple times.

!!! warning "Strong Passwords"
    Always use strong, unique passwords for admin accounts. Consider using a password manager.

## Tips & Tricks

!!! success "Command Shortcuts"
    Create shell aliases for common commands:
    
    ```bash
    # In ~/.bash_profile or ~/.zshrc
    alias jsweb-dev="jsweb run --reload --qr"
    alias jsweb-migrate="jsweb db prepare"
    alias jsweb-upgrade="jsweb db upgrade"
    ```

!!! tip "Working with Migrations"
    Good migration workflow:
    
    ```bash
    # Make changes to models
    # ...
    
    # Create migration
    jsweb db prepare -m "Descriptive message"
    
    # Test migration
    jsweb db upgrade
    
    # Commit changes
    git add -A
    git commit -m "Add migration: descriptive message"
    ```

!!! info "Environment Variables"
    Configure server via environment variables:
    
    ```bash
    # Using environment variables
    export JSWEB_HOST=0.0.0.0
    export JSWEB_PORT=5000
    jsweb run --reload
    ```

!!! note "Port Already in Use"
    If port 8000 is already in use:
    
    ```bash
    # Use different port
    jsweb run --port 8001
    
    # Or find and kill process
    lsof -i :8000     # Find process
    kill -9 <PID>     # Kill process
    ```

!!! tip "QR Code for Mobile Testing"
    Use `--qr` flag to quickly test on mobile devices:
    
    ```bash
    jsweb run --reload --qr
    # Then scan the QR code with your phone
    ```

