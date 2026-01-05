# Forms

JsWeb provides a powerful and easy-to-use form library that simplifies the process of handling user input and validation.

## Table of Contents

- [Creating a Form](#creating-a-form)
- [Form Fields](#form-fields)
- [Validators](#validators)
- [Rendering Forms](#rendering-forms)
- [Form Validation](#form-validation)
- [File Upload](#file-upload)
- [CSRF Protection](#csrf-protection)
- [Custom Validators](#custom-validators)
- [Best Practices](#best-practices)

## Creating a Form

To create a form, define a class that inherits from `jsweb.forms.Form`. Add fields as class attributes:

```python
from jsweb.forms import Form, StringField, PasswordField, HiddenField
from jsweb.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    csrf_token = HiddenField()
```

## Form Fields

JsWeb provides a variety of form fields for different input types:

### Text Fields

| Field | Description | Example |
|-------|-------------|---------|
| `StringField` | Single-line text input | `StringField("Name")` |
| `PasswordField` | Password input (hidden) | `PasswordField("Password")` |
| `TextAreaField` | Multi-line text input | `TextAreaField("Comments")` |
| `EmailField` | Email input | `EmailField("Email")` |
| `URLField` | URL input | `URLField("Website")` |
| `SearchField` | Search input | `SearchField("Search")` |

### Number & Boolean Fields

| Field | Description | Example |
|-------|-------------|---------|
| `IntegerField` | Integer input | `IntegerField("Age")` |
| `FloatField` | Decimal number input | `FloatField("Price")` |
| `DecimalField` | High-precision decimal | `DecimalField("Amount")` |
| `BooleanField` | Checkbox | `BooleanField("Agree to terms")` |

### Date & Time Fields

| Field | Description | Example |
|-------|-------------|---------|
| `DateField` | Date picker | `DateField("Birth Date")` |
| `TimeField` | Time picker | `TimeField("Start Time")` |
| `DateTimeField` | Date & time picker | `DateTimeField("Appointment")` |

### Selection Fields

| Field | Description | Example |
|-------|-------------|---------|
| `SelectField` | Dropdown list | `SelectField("Country", choices=[...])` |
| `RadioField` | Radio button group | `RadioField("Gender", choices=[...])` |
| `FileField` | File upload | `FileField("Upload")` |
| `HiddenField` | Hidden field (CSRF token) | `HiddenField()` |

### Complete Example

```python
from jsweb.forms import Form, StringField, IntegerField, SelectField, DateField, BooleanField
from jsweb.validators import DataRequired, Email, NumberRange

class UserRegistrationForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    age = IntegerField("Age", validators=[NumberRange(min=18, max=120)])
    country = SelectField("Country", choices=[
        ("us", "United States"),
        ("uk", "United Kingdom"),
        ("ca", "Canada")
    ])
    birth_date = DateField("Birth Date")
    newsletter = BooleanField("Subscribe to newsletter")
    csrf_token = HiddenField()
```

## Validators

Validators check that submitted data is valid. Pass a list of validators to the `validators` argument:

```python
from jsweb.validators import (
    DataRequired, Length, Email, EqualTo, NumberRange,
    FileRequired, FileAllowed, URL, Regexp
)

class Form(Form):
    username = StringField("Username", validators=[
        DataRequired(message="Username is required"),
        Length(min=4, max=25, message="Username must be 4-25 characters")
    ])
```

### Built-in Validators

| Validator | Purpose | Example |
|-----------|---------|---------|
| `DataRequired` | Field cannot be empty | `DataRequired()` |
| `Length` | String length validation | `Length(min=3, max=50)` |
| `Email` | Valid email format | `Email()` |
| `URL` | Valid URL format | `URL()` |
| `EqualTo` | Compare with another field | `EqualTo('password')` |
| `NumberRange` | Number within range | `NumberRange(min=0, max=100)` |
| `FileRequired` | File must be uploaded | `FileRequired()` |
| `FileAllowed` | Allowed file extensions | `FileAllowed(['pdf', 'doc'])` |
| `FileSize` | File size limit | `FileSize(max_size=5_000_000)` |
| `Regexp` | Match regex pattern | `Regexp(r'^[A-Z]')` |
| `Optional` | Field is optional | `Optional()` |

### Validator Examples

```python
class SignUpForm(Form):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=4, max=20)
    ])
    
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Invalid email address")
    ])
    
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8)
    ])
    
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    
    age = IntegerField("Age", validators=[
        NumberRange(min=18, message="Must be at least 18")
    ])
    
    website = StringField("Website (optional)", validators=[URL()])
```

!!! tip "Custom Messages"
    Provide custom validation error messages to improve user experience.

## Rendering Forms

Use the `render` function to pass the form to your template:

```python
from jsweb.response import render
from .forms import LoginForm

@app.route("/login", methods=["GET", "POST"])
async def login(req):
    form = LoginForm(await req.form(), await req.files())
    if req.method == "POST" and form.validate():
        # Handle the login
        username = form.username.data
        # ... authentication logic ...
    return render(req, "login.html", {"form": form})
```

## Form Validation

### Checking if Form is Valid

```python
if form.validate():
    # Process form data
    data = form.data  # All form data as dictionary
    username = form.username.data
else:
    # Form has errors
    errors = form.errors  # Dictionary of field errors
```

### Accessing Field Data

```python
# Get specific field value
username = form.username.data

# Get all form data
all_data = form.data  # Returns dict

# Check if field has errors
if form.username.errors:
    print(form.username.errors)  # List of error messages
```

### Rendering in Template

```html
<!-- templates/login.html -->
<form method="post" enctype="multipart/form-data">
    {{ form.csrf_token() }}
    
    <div class="form-group">
        {{ form.username.label }}
        {{ form.username() }}
        {% if form.username.errors %}
            <div class="errors">
                {% for error in form.username.errors %}
                    <p>{{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <div class="form-group">
        {{ form.password.label }}
        {{ form.password() }}
        {% if form.password.errors %}
            <div class="errors">
                {% for error in form.password.errors %}
                    <p>{{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <button type="submit">Log In</button>
</form>
```

### Styling with CSS

```css
.errors {
    color: #d32f2f;
    margin-top: 0.5rem;
}

.form-group {
    margin-bottom: 1rem;
}

input.error {
    border-color: #d32f2f;
}
```

## File Upload

Handle file uploads with `FileField`:

```python
from jsweb.forms import Form, FileField, StringField
from jsweb.validators import FileRequired, FileAllowed

class ProfileForm(Form):
    bio = StringField("Bio")
    avatar = FileField("Profile Picture", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'])
    ])
```

### Processing File Uploads

```python
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@app.route("/upload", methods=["GET", "POST"])
async def upload_profile(req):
    form = ProfileForm(await req.form(), await req.files())
    
    if req.method == "POST" and form.validate():
        file = form.avatar.data
        
        # Secure the filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file
        file.save(filepath)
        
        return "File uploaded successfully!"
    
    return render(req, "upload.html", {"form": form})
```

!!! warning "Security"
    Always validate file uploads using `FileAllowed` and `secure_filename()` to prevent security vulnerabilities.

## CSRF Protection

JsWeb provides built-in CSRF protection. Include a hidden `csrf_token` field in your forms:

```python
class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    csrf_token = HiddenField()  # Required for CSRF protection
```

### In Templates

```html
<form method="post">
    {{ form.csrf_token() }}
    <!-- Rest of form fields -->
</form>
```

!!! info "CSRF Token Validation"
    JsWeb automatically validates CSRF tokens on POST requests. Always include the `csrf_token` field in your forms.

!!! note "Future API Header Support"
    Future versions of JsWeb will support sending the CSRF token in the `X-CSRF-Token` HTTP header for SPAs and API-first applications.

## Custom Validators

Create custom validators for specific validation logic:

```python
from jsweb.validators import ValidationError

def validate_username_available(form, field):
    """Check if username is not already taken"""
    from .models import User
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already taken')

def validate_no_special_chars(form, field):
    """Check that field contains no special characters"""
    import re
    if not re.match(r'^[a-zA-Z0-9_]+$', field.data):
        raise ValidationError('Only alphanumeric and underscore allowed')

class SignUpForm(Form):
    username = StringField("Username", validators=[
        DataRequired(),
        validate_username_available
    ])
    
    bio = TextAreaField("Bio", validators=[
        validate_no_special_chars
    ])
```

!!! tip "Validation Order"
    Built-in validators run first, then custom validators. Place custom validators last in the list.

## Best Practices

!!! warning "Always Validate Input"
    Never trust user input. Always validate on the server side, even if you have client-side validation:
    
    ```python
    if form.validate():
        # Safe to use form.data
    ```

!!! tip "Use Specific Field Types"
    Use the most specific field type for better semantics:
    
    ```python
    # Good
    email = EmailField("Email", validators=[Email()])
    age = IntegerField("Age")
    
    # Less good
    email = StringField("Email")
    age = StringField("Age")
    ```

!!! info "Security: Password Fields"
    Always use `PasswordField` for passwords, never `StringField`:
    
    ```python
    # Good
    password = PasswordField("Password")
    
    # Bad
    password = StringField("Password")  # Not hidden!
    ```

!!! note "Flash Messages"
    Provide user feedback after form submission:
    
    ```python
    if form.validate():
        # Process form
        return redirect("/success")
    else:
        # Show validation errors
        return render(req, "form.html", {"form": form})
    ```

!!! tip "Organize Large Forms"
    Break large forms into multiple steps or use field groups:
    
    ```python
    class CheckoutForm(Form):
        # Billing information
        billing_address = StringField("Address")
        
        # Shipping information
        shipping_address = StringField("Address")
        
        # Payment information
        card_number = StringField("Card Number")
    ```

