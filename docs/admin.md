# Admin Interface

JsWeb includes a built-in admin interface that allows you to manage your application's data. The admin interface is automatically generated based on your models and is ready for production use out of the box.

## Table of Contents

- [Enabling the Admin Interface](#enabling-the-admin-interface)
- [Creating Admin Users](#creating-admin-users)
- [Accessing the Admin Panel](#accessing-the-admin-panel)
- [Managing Models](#managing-models)
- [Admin Features](#admin-features)
- [Security Considerations](#security-considerations)
- [Customization](#customization)
- [Best Practices](#best-practices)

## Enabling the Admin Interface

To enable the admin interface, create an `Admin` instance and register your models with it:

```python
# app.py
from jsweb import JsWebApp
from jsweb.admin import Admin
from .models import User, Post, Category
import config

app = JsWebApp(config=config)

# Create admin instance
admin = Admin(app)

# Register your models
admin.register(User)
admin.register(Post)
admin.register(Category)
```

This will create an admin interface accessible at `/admin`.

!!! tip "Auto-Generated Admin"
    The admin interface is completely auto-generated based on your models. No additional configuration needed!

## Creating Admin Users

Before you can access the admin interface, you need to create an admin user:

```bash
jsweb create-admin
```

This command will prompt you to enter:
- **Username**: Your admin username
- **Email**: Your admin email address
- **Password**: A secure password

### Creating Admin Users Programmatically

```python
from .models import User

# Create admin user with code
admin_user = User.create(
    username="admin",
    email="admin@example.com",
    password="secure_password",
    is_admin=True
)
```

!!! warning "Security"
    Always use strong passwords. Never hardcode credentials in your application.

## Accessing the Admin Panel

Once an admin user is created, you can access the admin panel:

1. Navigate to `http://your-domain.com/admin`
2. Log in with your admin credentials
3. Manage your application's data

## Managing Models

### Viewing Records

The admin interface displays all records in a table format:
- **List View**: See all records with key fields
- **Search**: Find specific records
- **Filtering**: Filter records by field values
- **Sorting**: Sort by any column

### Creating Records

Click the "Add" or "Create" button to add a new record. A form will appear with all model fields.

### Editing Records

Click on any record in the list to edit its details. The edit form displays:
- All model fields
- Field values
- Validation errors (if any)

### Deleting Records

Click the delete button to remove a record. A confirmation will appear before deletion.

## Admin Features

### Automatic Field Detection

The admin interface automatically detects your model fields and displays appropriate widgets:

| Field Type | Widget |
|-----------|--------|
| String | Text input |
| Integer | Number input |
| Float | Decimal input |
| Date | Date picker |
| DateTime | Date & time picker |
| Boolean | Checkbox |
| Text | Textarea |
| Foreign Key | Dropdown selector |

### Search & Filter

The admin interface provides:
- **Full-text search** across all fields
- **Field filtering** by specific values
- **Boolean filtering** for true/false fields
- **Relationship filtering** for foreign keys

### Bulk Actions

Perform operations on multiple records:
- Select multiple records
- Apply actions (delete, export, etc.)

## Security Considerations

!!! warning "Admin Access Control"
    The admin interface should only be accessible to trusted administrators. Consider:
    
    - Using strong passwords
    - Enabling 2FA (if available)
    - Restricting IP access with a proxy/firewall
    - Using HTTPS in production

!!! danger "Data Protection"
    Be careful when deleting records. Deletions are usually permanent. Consider implementing:
    
    ```python
    # Soft delete approach
    class Post(ModelBase):
        __tablename__ = 'posts'
        title = Column(String(200))
        deleted_at = Column(DateTime, nullable=True)
        
        @property
        def is_deleted(self):
            return self.deleted_at is not None
    ```

!!! note "Audit Logging"
    Consider adding audit logs to track admin actions:
    
    ```python
    class AuditLog(ModelBase):
        __tablename__ = 'audit_logs'
        admin_id = Column(Integer, ForeignKey('user.id'))
        action = Column(String(100))
        model_name = Column(String(100))
        record_id = Column(Integer)
        timestamp = Column(DateTime, default=datetime.utcnow)
    ```

## Customization

### Limiting Model Fields

```python
# Currently not available in base Admin class
# Feature for future versions
```

### Custom Model Lists

```python
# Custom template override support
# Feature for future versions
```

!!! info "Future Customization"
    More customization options are planned for future versions, such as:
    - Custom column lists
    - Custom filters
    - Inline editing
    - Bulk operations

## Best Practices

!!! tip "Model Organization"
    Keep your models organized in `models.py`:
    
    ```python
    # models.py
    from jsweb.database import ModelBase, Column, Integer, String
    
    class User(ModelBase):
        __tablename__ = 'users'
        # ... fields ...
    
    class Post(ModelBase):
        __tablename__ = 'posts'
        # ... fields ...
    
    # app.py
    from models import User, Post
    admin.register(User)
    admin.register(Post)
    ```

!!! warning "Register Models Early"
    Register admin models right after creating the Admin instance:
    
    ```python
    admin = Admin(app)
    
    # Register all models
    admin.register(User)
    admin.register(Post)
    admin.register(Category)
    
    # Then define routes
    @app.route("/")
    async def home(req):
        ...
    ```

!!! success "Use Descriptive Names"
    Use clear, descriptive model names for the admin interface:
    
    ```python
    # Good
    class BlogPost(ModelBase):
        __tablename__ = 'blog_posts'
    
    # Less clear
    class P(ModelBase):
        __tablename__ = 'p'
    ```

!!! tip "Validation in Models"
    Add validation to your models for better data quality:
    
    ```python
    class User(ModelBase):
        __tablename__ = 'users'
        username = Column(String(80), unique=True, nullable=False)
        email = Column(String(120), unique=True, nullable=False, index=True)
        
        def __repr__(self):
            return f"<User {self.username}>"
    ```

!!! note "Admin vs Public Interface"
    Keep admin interface separate from public-facing pages:
    
    ```
    routes/
    ├── public_routes.py      # Public pages
    ├── auth_routes.py        # Login/Register
    ├── api_routes.py         # API endpoints
    └── admin_routes.py       # Admin-only routes (if needed)
    ```

