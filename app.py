from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load .env variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Authentication API"}
)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

# Register blueprints
from application.routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
from application.routes.product_routes import product_bp
app.register_blueprint(product_bp)
from application.routes.institution_routes import institution_bp
app.register_blueprint(institution_bp)
from application.routes.iot_device_routes import iot_device_bp
app.register_blueprint(iot_device_bp)
from application.routes.api_access_routes import api_access_bp
app.register_blueprint(api_access_bp)


# Ensure database tables are created
first_request = True

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Welcome to Flask Authentication API"}

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")
