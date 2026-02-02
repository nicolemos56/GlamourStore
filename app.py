import os
import logging
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if not database_url or "ep-calm-shadow-a5nmejk6.us-east-2.aws.neon.tech" in database_url:
    # Fallback to SQLite if PostgreSQL is not available or using disabled Neon endpoint
    database_url = "sqlite:///nc_glamourstore.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
else:
    # For Render, fix postgresql:// URLs to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'djmeagtqv'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '224513256814989'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'MFXEYMfdKOZkkvW6HsO9lPWBua8')
)

# Configure upload settings
app.config['UPLOAD_FOLDER'] = 'static/images/products'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_cloudinary(file):
    """Upload file to Cloudinary and return the URL"""
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="nc_glamourstore/products",
            transformation=[
                {'width': 800, 'height': 800, 'crop': 'limit'},
                {'quality': 'auto'}
            ]
        )
        return result['secure_url']
    except Exception as e:
        logging.error(f"Erro no upload para Cloudinary: {e}")
        return None

# Initialize the app with the extension
db.init_app(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"  # type: ignore
login_manager.login_message = "Por favor, faça login para acessar esta página."

# Initialize session cart if not exists
@app.before_request
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

with app.app_context():
    # Import models to ensure tables are created
    from models import User, Product, Order, OrderItem, Category
    
    # Create all tables
    db.create_all()
    
    # Initialize default data
    from database import init_default_data
    init_default_data()

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import routes
from routes import *
if __name__ == "__main__":
    app.run()

