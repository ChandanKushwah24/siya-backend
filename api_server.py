from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from functools import wraps


def auth_required(refresh=False):
    """Custom decorator for JWT authentication with optional refresh token support. 
    """
    def wrapper(f):
        @jwt_required(refresh=refresh)
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = get_jwt_identity()
            if not current_user:
                return {'message': 'Unauthorized access - invalid or missing token', 'error': True}, 401
            return f(*args, **kwargs)
        return decorated
    return wrapper


# Initialize API Blueprint with versioning
newBlueprint = Blueprint('v1', __name__, url_prefix='/api')

# Configure Swagger UI authentication
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(newBlueprint,
          title='Pitch Deck Editor API',
          version='1.0',
          description='API for managing presentation slides with customizable templates and themes',
          authorizations=authorizations,
         security='Bearer Auth'
          )


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Factory function to create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance ready for use
    
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app) 
    with app.app_context():

        import apis.users.user
        import apis.slides.slide

        app.register_blueprint(newBlueprint)
        
        CORS(app)

        return app
