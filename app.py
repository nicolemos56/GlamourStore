import os
import logging
import sqlite3
from flask import Flask, session
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# Database configuration for SQLite
DATABASE_PATH = 'nc_glamourstore.db'

# Initialize session cart if not exists
@app.before_request
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

# Flask-Login user loader
from database import AdminUser

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.get(int(user_id))

# Initialize database on startup
from database import init_database
init_database()

# Import routes
from routes import *


