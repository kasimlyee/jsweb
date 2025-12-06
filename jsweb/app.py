import secrets
import os
from .routing import Router
from .request import Request
from .response import Response, HTMLResponse, configure_template_env
from .auth import init_auth, get_current_user
from .middleware import StaticFilesMiddleware, DBSessionMiddleware, CSRFMiddleware
from .blueprints import Blueprint

class JsWebApp:
    """
    The main application class for the JsWeb framework.
    """
    def __init__(self, config):
        self.router = Router()
        self.template_filters = {}
        self.config = config
        self.blueprints_with_static_files = []
        self._init_from_config()  # Initial setup

    def _init_from_config(self):
        """Initializes components that depend on the config."""
        template_paths = []

        # Add the user's template folder
        if hasattr(self.config, "TEMPLATE_FOLDER") and hasattr(self.config, "BASE_DIR"):
            user_template_path = os.path.join(self.config.BASE_DIR, self.config.TEMPLATE_FOLDER)
            if os.path.isdir(user_template_path):
                template_paths.append(user_template_path)

        # Add the library's main template folder
        lib_template_path = os.path.join(os.path.dirname(__file__), "templates")
        if os.path.isdir(lib_template_path):
            template_paths.append(lib_template_path)
            
        # Add the library's admin template folder
        admin_template_path = os.path.join(os.path.dirname(__file__), "admin_templates")
        if os.path.isdir(admin_template_path):
            template_paths.append(admin_template_path)

        if template_paths:
            configure_template_env(template_paths)

        if hasattr(self.config, "SECRET_KEY"):
            init_auth(self.config.SECRET_KEY, self._get_actual_user_loader())

    def _get_actual_user_loader(self):
        if hasattr(self, '_user_loader_callback') and self._user_loader_callback:
            return self._user_loader_callback
        return self.user_loader

    def user_loader(self, user_id: int):
        try:
            from models import User
            return User.query.get(user_id)
        except (ImportError, AttributeError):
            return None

    def route(self, path, methods=None, endpoint=None):
        return self.router.route(path, methods, endpoint)

    def register_blueprint(self, blueprint: Blueprint):
        """Registers a blueprint with the application."""
        for path, handler, methods, endpoint in blueprint.routes:
            full_path = path
            if blueprint.url_prefix:
                full_path = f"{blueprint.url_prefix.rstrip('/')}/{path.lstrip('/')}"
            
            full_endpoint = f"{blueprint.name}.{endpoint}"
            self.router.add_route(full_path, handler, methods, endpoint=full_endpoint)

        if blueprint.static_folder:
            self.blueprints_with_static_files.append(blueprint)

    def filter(self, name):
        def decorator(func):
            self.template_filters[name] = func
            return func
        return decorator

    def _wsgi_app_handler(self, environ, start_response):
        req = environ['jsweb.request']

        handler, params = self.router.resolve(req.path, req.method)
        if handler:
            response = handler(req, **params)

            if isinstance(response, str):
                response = HTMLResponse(response)

            if not isinstance(response, Response):
                raise TypeError(f"View function did not return a Response object (got {type(response).__name__})")

            if hasattr(req, 'new_csrf_token_generated') and req.new_csrf_token_generated:
                response.set_cookie("csrf_token", req.csrf_token, httponly=False, samesite='Lax')

            body_bytes, status, headers = response.to_wsgi()
            start_response(status, headers)
            return [body_bytes]

        start_response("404 Not Found", [("Content-Type", "text/html")])
        return [b"<h1>404 Not Found</h1>"]

    def __call__(self, environ, start_response):
        req = Request(environ, self)
        environ['jsweb.request'] = req

        csrf_token = req.cookies.get("csrf_token")
        req.new_csrf_token_generated = False
        if not csrf_token:
            csrf_token = secrets.token_hex(32)
            req.new_csrf_token_generated = True
        req.csrf_token = csrf_token

        if hasattr(self.config, "SECRET_KEY"):
            req.user = get_current_user(req)

        static_url = getattr(self.config, "STATIC_URL", "/static")
        static_dir = getattr(self.config, "STATIC_DIR", "static")
        
        handler = self._wsgi_app_handler
        handler = DBSessionMiddleware(handler)
        # Pass blueprint static file info to the middleware
        handler = StaticFilesMiddleware(handler, static_url, static_dir, blueprint_statics=self.blueprints_with_static_files)
        handler = CSRFMiddleware(handler)

        return handler(environ, start_response)
