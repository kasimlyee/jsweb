# config.py
import os

APP_NAME = "Test1"
DEBUG = True
VERSION = "0.1.0"
SECRET_KEY = "dae115d9914a8a93602d09dc86c87797"  # Crucial for session security
TEMPLATE_FOLDER = "templates"
STATIC_URL = "/static"
STATIC_DIR = "static"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'jsweb.db')}"
HOST = "127.0.0.1"
PORT = 8000