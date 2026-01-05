# Blueprints

Blueprints are a way to organize your JsWeb application into smaller, reusable components. A blueprint is a collection of routes that can be registered with your main application. This is an essential pattern for structuring larger applications.

## Table of Contents

- [What are Blueprints?](#what-are-blueprints)
- [Creating a Blueprint](#creating-a-blueprint)
- [Registering Blueprints](#registering-blueprints)
- [URL Prefixes](#url-prefixes)
- [Static Files & Templates](#static-files--templates)
- [Nested Blueprints](#nested-blueprints)
- [Best Practices](#best-practices)

## What are Blueprints?

Blueprints allow you to:
- **Organize code** into logical modules (auth, admin, API, etc.)
- **Reuse components** across multiple applications
- **Scale applications** as they grow
- **Maintain separation of concerns** with clear folder structure

## Creating a Blueprint

To create a blueprint, import the `Blueprint` class and define routes on it:

**`views.py`**
```python
from jsweb import Blueprint, render

# 1. Create a "Blueprint" for a group of related pages.
views_bp = Blueprint('views')

# 2. Define a route on the blueprint.
@views_bp.route("/")
async def home(req):
    # The render function automatically finds your templates.
    return render(req, "welcome.html", {"user_name": "Guest"})

@views_bp.route("/about")
async def about(req):
    return render(req, "about.html")
```

## Registering Blueprints

Once you've created a blueprint, register it with your main application:

**`app.py`**
```python
from jsweb import JsWebApp
import config

# Import the blueprint you just created.
from views import views_bp

# 3. Create the main application instance.
app = JsWebApp(config=config)

# 4. Register your blueprint with the app.
app.register_blueprint(views_bp)
```

!!! tip "Multiple Blueprints"
    You can register multiple blueprints with your application. Each blueprint maintains its own namespace of routes.

## URL Prefixes

Add a URL prefix to all routes in a blueprint:

```python
# auth/routes.py
auth_bp = Blueprint('auth', url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
async def login(req):
    return render(req, "auth/login.html")

@auth_bp.route('/logout')
async def logout(req):
    # Handle logout
    return redirect('/')

@auth_bp.route('/register', methods=['GET', 'POST'])
async def register(req):
    return render(req, "auth/register.html")
```

When you register this blueprint, the routes will be available at:
- `/auth/login`
- `/auth/logout`
- `/auth/register`

### Registering with Prefix

You can also specify a prefix when registering:

```python
# app.py
from auth.routes import auth_bp

app = JsWebApp(config=config)
app.register_blueprint(auth_bp, url_prefix='/api/v1')
```

This will make routes available at `/api/v1/auth/login`, etc.

## Static Files & Templates

Blueprints can have their own static files and templates.

### Project Structure

```
myapp/
├── app.py
├── views/
│   ├── routes.py
│   ├── templates/
│   │   └── views/
│   │       ├── home.html
│   │       └── about.html
│   └── static/
│       └── views/
│           └── views.css
├── admin/
│   ├── routes.py
│   ├── templates/
│   │   └── admin/
│   │       └── dashboard.html
│   └── static/
│       └── admin/
│           └── admin.css
└── config.py
```

### Creating Blueprints with Static & Templates

```python
# admin/routes.py
from jsweb import Blueprint, render

admin_bp = Blueprint(
    'admin',
    url_prefix='/admin',
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)

@admin_bp.route('/dashboard')
async def dashboard(req):
    # Uses admin/templates/dashboard.html
    return render(req, 'dashboard.html')
```

!!! tip "Template Organization"
    Within `template_folder`, create subdirectories matching your blueprint name for clarity.

## Nested Blueprints

Organize related functionality with nested blueprints:

```python
# users/routes.py
from jsweb import Blueprint, render

users_bp = Blueprint('users', url_prefix='/users')

@users_bp.route('/')
async def user_list(req):
    return render(req, "users/list.html")

@users_bp.route('/<int:user_id>')
async def user_detail(req, user_id):
    return render(req, "users/detail.html", {"user_id": user_id})

@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
async def user_edit(req, user_id):
    return render(req, "users/edit.html", {"user_id": user_id})

# api/routes.py
from jsweb import Blueprint
from users.routes import users_bp

api_bp = Blueprint('api', url_prefix='/api/v1')
api_bp.register_blueprint(users_bp)

# app.py
from api.routes import api_bp

app.register_blueprint(api_bp)
```

Routes will be available at:
- `/api/v1/users/`
- `/api/v1/users/<user_id>`
- `/api/v1/users/<user_id>/edit`

## Best Practices

!!! tip "Blueprint Organization"
    Organize your blueprints logically:
    
    ```
    myapp/
    ├── app.py
    ├── config.py
    ├── views/              # Public views
    ├── auth/               # Authentication
    ├── admin/              # Admin panel
    ├── api/                # API endpoints
    └── core/               # Shared utilities
    ```

!!! warning "Avoid Circular Imports"
    Be careful not to create circular imports when importing blueprints. Structure your imports carefully:
    
    ```python
    # Good: Import blueprint in app.py
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Avoid: Don't import app in blueprint module
    # from app import app  # Bad!
    ```

!!! info "Blueprint Naming"
    Use clear, descriptive blueprint names:
    
    ```python
    auth_bp = Blueprint('auth')        # ✓ Good
    bp = Blueprint('bp')               # ✗ Not descriptive
    ```

!!! tip "Shared Templates & Static"
    Create a `core` or `base` blueprint for shared templates and assets:
    
    ```python
    # core/routes.py
    core_bp = Blueprint('core', template_folder='templates')
    
    # Place shared templates in core/templates/
    # - base.html
    # - macros.html
    # - components/
    ```

!!! note "Blueprint Methods"
    Blueprints support the same decorators as the app:
    
    ```python
    @bp.route('/path')
    @bp.before_request
    @bp.after_request
    @bp.errorhandler(404)
    @bp.filter('custom_filter')
    ```

!!! success "Testing Blueprints"
    Blueprints are easier to test in isolation:
    
    ```python
    # test_auth.py
    from auth.routes import auth_bp
    
    # Create test app with just auth blueprint
    test_app = JsWebApp(config=test_config)
    test_app.register_blueprint(auth_bp)
    ```

