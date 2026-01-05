---
hide:
  - navigation
  - toc
---

<style>
  .md-typeset h1 {
    display: none;
  }
</style>

<p align="center">
  <img src="https://github.com/Jsweb-Tech/jsweb/blob/main/images/jsweb-main-logo.png?raw=true" alt="JsWeb Logo" width="200">
</p>

<p align="center" style="font-size: 1.3em; font-weight: 500; margin-bottom: 0.5em;">
    <strong>The Blazing-Fast, Modern ASGI Python Web Framework</strong>
</p>

<p align="center" style="font-size: 1em; color: #666; margin-bottom: 1.5em;">
    Build full-stack web apps and APIs with zero JavaScript. Pure Python, pure speed.
</p>

<p align="center">
<a href="https://pypi.org/project/jsweb/" target="_blank">
    <img src="https://img.shields.io/pypi/v/jsweb?color=%2334D058&label=pypi%20package" alt="PyPI version">
</a>
<a href="https://pypi.org/project/jsweb/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/jsweb.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/Jsweb-Tech/jsweb/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/Jsweb-Tech/jsweb.svg?color=%2334D058" alt="License">
</a>
<a href="https://pepy.tech/project/Jsweb" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/jsweb?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLUE&right_color=GREEN&left_text=downloads" alt="Downloads">
</a>
</p>

<p align="center" style="margin-top: 1em;">
  <a href="https://discord.gg/cqg5wgEVhP" target="_blank">
    <img src="https://gist.githubusercontent.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/discord.svg" alt="Discord"/>
  </a>
  <a href="https://jsweb-framework.site" target="_blank">
    <img src="https://gist.githubusercontent.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/documentation_learn.svg" alt="Documentation"/>
  </a>
  <a href="https://github.com/Jsweb-Tech/jsweb" target="_blank">
    <img src="https://gist.githubusercontent.com/cxmeel/0dbc95191f239b631c3874f4ccf114e2/raw/github_sponsor.svg" alt="GitHub"/>
  </a>
</p>

---

<p align="center" style="font-size: 1.5em; font-weight: 600; margin: 1.5em 0;">
  💝 Sponsors 💝
</p>

<p align="center" style="font-size: 1.1em; color: #666; margin: 1.5em 0;">
  As of now we don't have any sponsors
</p>

<p align="center" style="font-size: 0.95em; color: #888; margin: 1em 0;">
  Love JsWeb? Help us keep the project alive and growing! We're looking for sponsors to support ongoing development.
</p>

<p align="center">
  <a href="https://github.com/sponsors/Jones-peter" target="_blank" style="display: inline-block; margin: 0.5em; padding: 0.75em 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);">
    💖 Sponsor on GitHub
  </a>
  <a href="https://www.paypal.com/paypalme/jonespeter22" target="_blank" style="display: inline-block; margin: 0.5em; padding: 0.75em 1.5em; background: linear-gradient(135deg, #0070ba 0%, #003087 100%); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 2px 8px rgba(0, 112, 186, 0.3);">
    💳 Donate on PayPal
  </a>
</p>

---

## ✨ Why JsWeb?

### Modern Architecture
Built on **ASGI** for blazing-fast performance and true async support. Handle thousands of concurrent connections effortlessly.

### Zero Configuration
- **Automatic AJAX**: Forms and navigation work like a Single Page Application—without writing JavaScript
- **Built-in Admin Panel**: Production-ready interface generated automatically from your models
- **Automatic API Docs**: OpenAPI 3.0.3 documentation generated at `/docs` and `/redoc`

### Developer First
- **Simple Routing**: Elegant decorator-based route definition
- **Powerful CLI**: Create projects, manage migrations, and run your server with simple commands
- **Modular Blueprints**: Organize code into reusable, maintainable components
- **Full-Featured Forms**: Validation, CSRF protection, and file uploads built-in

### Production Ready
- **Security Built-in**: CSRF protection, secure sessions, password hashing
- **Database Support**: SQLAlchemy with Alembic migrations for any SQL database
- **Jinja2 Templates**: Powerful templating for dynamic HTML rendering
- **Modular Design**: Scale from single-file apps to enterprise applications

---

## 🚀 Quick Start (30 seconds)

### 1. Install

```bash
pip install jsweb
```

### 2. Create Project

```bash
jsweb new my_project
cd my_project
```

### 3. Run

```bash
jsweb run --reload
```

That's it! Visit **http://127.0.0.1:8000** and your app is live! 🎉

---

## 💡 See It In Action

**`views.py`** - Define your routes
```python
from jsweb import Blueprint, render

views_bp = Blueprint('views')

@views_bp.route("/")
async def home(req):
    return render(req, "welcome.html", {"user_name": "Guest"})

@views_bp.route("/api/status")
async def status(req):
    return {"status": "online", "message": "Hello from JsWeb!"}
```

**`app.py`** - Wire it all together
```python
from jsweb import JsWebApp
from views import views_bp
import config

app = JsWebApp(config=config)
app.register_blueprint(views_bp)
```

That's all you need for a working full-stack application!

---

## 📊 Key Features at a Glance

| Feature | Benefit |
|---------|---------|
| 🚀 **ASGI Framework** | Lightning-fast async I/O, handles thousands of requests |
| 🔄 **Zero-Config AJAX** | Forms and navigation work like SPAs, no JavaScript needed |
| 🗄️ **SQLAlchemy + Alembic** | Powerful ORM with seamless migrations |
| 🛡️ **Security Built-in** | CSRF, secure sessions, password hashing by default |
| ⚙️ **Auto Admin Panel** | Production-ready data management interface |
| 🧩 **Blueprints** | Organize code into modular, reusable components |
| 🎨 **Jinja2 Templates** | Powerful template engine with inheritance and macros |
| 📚 **Auto API Docs** | OpenAPI documentation generated automatically |
| 🛠️ **Powerful CLI** | Project scaffolding, server, migrations all in one |
| 📱 **Responsive** | Works beautifully on all devices |

---

## 📖 Next Steps

Ready to build your next amazing project?

<p align="center">
  <a href="getting-started.md" style="display: inline-block; margin: 0.5em; padding: 0.75em 1.5em; background: #2196f3; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
    📚 Get Started Guide
  </a>
  <a href="https://github.com/Jsweb-Tech/jsweb" target="_blank" style="display: inline-block; margin: 0.5em; padding: 0.75em 1.5em; background: #333; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
    🔧 View Source Code
  </a>
  <a href="https://discord.gg/cqg5wgEVhP" target="_blank" style="display: inline-block; margin: 0.5em; padding: 0.75em 1.5em; background: #5865f2; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">
    💬 Join Community
  </a>
</p>

---

## 📚 Complete Documentation

Explore detailed guides and references:

- **[Getting Started](getting-started.md)** - Installation, setup, and your first app
- **[Routing](routing.md)** - URL mapping and HTTP methods
- **[Database](database.md)** - Models, queries, and migrations
- **[Templating](templating.md)** - Jinja2 templates and filters
- **[Forms](forms.md)** - Form handling and validation
- **[Blueprints](blueprints.md)** - Modular application architecture
- **[Admin Panel](admin.md)** - Data management interface
- **[CLI Reference](cli.md)** - Command-line tools

---

## 🤝 Community & Support

- **GitHub**: [Jsweb-Tech/jsweb](https://github.com/Jsweb-Tech/jsweb)
- **Discord**: [Join our community](https://discord.gg/cqg5wgEVhP)
- **Issues**: [Report bugs or request features](https://github.com/Jsweb-Tech/jsweb/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/Jsweb-Tech/jsweb/discussions)

---

## 📄 License

JsWeb is licensed under the **MIT License** - free for personal and commercial use.

---

