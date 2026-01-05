# Configuration

JsWeb applications are configured using a `config.py` file in your project's root directory. This file contains all the settings your application needs to run, such as the database connection string, secret key, security settings, and other options.

## Table of Contents

- [Config File Structure](#config-file-structure)
- [Core Configuration Options](#core-configuration-options)
- [Database Configuration](#database-configuration)
- [Security Settings](#security-settings)
- [Development vs Production](#development-vs-production)
- [Environment Variables](#environment-variables)
- [Best Practices](#best-practices)

## Config File Structure

A new project created with `jsweb new` will have a default `config.py` file:

```python
import os

# Get the base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for signing sessions and other security-related things
SECRET_KEY = "your-secret-key"

# Database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Static files configuration
STATIC_URL = "/static"
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Template files configuration
TEMPLATE_FOLDER = "templates"
```

## Core Configuration Options

Here are the most important configuration options:

| Setting | Type | Description |
|---------|------|-------------|
| `SECRET_KEY` | String | Secret key for session signing and CSRF protection |
| `DEBUG` | Boolean | Enable/disable debug mode |
| `TESTING` | Boolean | Enable/disable testing mode |
| `SQLALCHEMY_DATABASE_URI` | String | Database connection string |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | Boolean | Track SQLAlchemy object modifications |
| `STATIC_URL` | String | URL prefix for static files |
| `STATIC_DIR` | String | Directory path for static files |
| `TEMPLATE_FOLDER` | String | Directory for templates |
| `MAX_CONTENT_LENGTH` | Integer | Maximum upload file size in bytes |

## Database Configuration

### SQLite (Development)

Perfect for local development and small projects:

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### PostgreSQL (Production)

Recommended for production applications:

```python
import os

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
}
```

### MySQL

```python
SQLALCHEMY_DATABASE_URI = (
    f"mysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)
```

### MariaDB

```python
SQLALCHEMY_DATABASE_URI = (
    f"mariadb://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)
```

!!! note "Connection Strings"
    Always use environment variables for sensitive database credentials. Never hardcode passwords in your config file.

## Security Settings

### Secret Key

The `SECRET_KEY` is used for signing sessions and protecting against CSRF attacks:

```python
import os
import secrets

# Generate a secure secret key
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
```

!!! danger "Secret Key Security"
    - Never commit your actual secret key to version control
    - Use a different key in production
    - Generate a new key with `secrets.token_hex(32)`
    - Store it in environment variables or a `.env` file

### HTTPS & Session Security

```python
# Enable HTTPS only cookies in production
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# CSRF Protection
WTF_CSRF_ENABLED = True
WTF_CSRF_SSL_STRICT = not DEBUG
```

## Development vs Production

### Development Configuration

```python
# config_dev.py
import os

DEBUG = True
TESTING = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "dev-secret-key-not-secure"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "dev.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True  # Helpful for development

STATIC_URL = "/static"
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_FOLDER = "templates"

# File uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
```

### Production Configuration

```python
# config_prod.py
import os

DEBUG = False
TESTING = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
}

STATIC_URL = "/static"
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_FOLDER = "templates"

# Security settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"

# File uploads
UPLOAD_FOLDER = "/var/uploads"
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

# Cache configuration
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300
```

### Using Environment-Based Config

```python
# config.py
import os

env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    from config_prod import *
else:
    from config_dev import *
```

## Environment Variables

Create a `.env` file for development:

```bash
# .env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///app.db
DEBUG=True
```

Load environment variables in your app:

```python
# app.py
import os
from dotenv import load_dotenv

load_dotenv()

import config
from jsweb import JsWebApp

app = JsWebApp(config=config)
```

!!! warning ".env File Safety"
    Add `.env` to `.gitignore` to prevent committing sensitive data:
    
    ```bash
    # .gitignore
    .env
    .env.local
    *.db
    __pycache__/
    ```

## Accessing Configuration

Access your configuration in your application:

```python
# app.py
from jsweb import JsWebApp
import config

app = JsWebApp(config=config)

# Access config
secret_key = app.config.SECRET_KEY
debug = app.config.DEBUG
db_uri = app.config.SQLALCHEMY_DATABASE_URI
```

### In Routes

```python
@app.route("/config-info")
async def config_info(req):
    return {
        "debug": app.config.DEBUG,
        "max_upload_size": app.config.MAX_CONTENT_LENGTH,
    }
```

## Best Practices

!!! warning "Never Hardcode Secrets"
    Always use environment variables for sensitive data:
    
    ```python
    # Bad
    SECRET_KEY = "my-secret-key"
    DB_PASSWORD = "password123"
    
    # Good
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    ```

!!! tip "Config Organization"
    Separate configs by environment:
    
    ```
    config/
    ├── __init__.py
    ├── base.py          # Common settings
    ├── development.py   # Dev-only settings
    ├── production.py    # Production settings
    └── testing.py       # Test settings
    ```

!!! info "Configuration Inheritance"
    Use a base config class to reduce duplication:
    
    ```python
    # config/base.py
    class Config:
        SECRET_KEY = os.getenv('SECRET_KEY')
        DEBUG = False
    
    # config/development.py
    class DevConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    
    # config/production.py
    class ProdConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    ```

!!! note "Validation"
    Validate your configuration on startup:
    
    ```python
    # app.py
    def validate_config(app):
        required = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
        for key in required:
            if not hasattr(app.config, key):
                raise ValueError(f"Missing configuration: {key}")
    
    validate_config(app)
    ```

!!! success "Local Override"
    Create a `config.local.py` for local overrides:
    
    ```python
    # config.py
    try:
        from config.local import *
    except ImportError:
        pass
    ```

