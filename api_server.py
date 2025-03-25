from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields
from config import Config
from flask_mail import Mail,Message
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create blueprint
newBlueprint = Blueprint('v1', __name__)
# Add authorization to swagger-ui
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
          doc='/api',
          authorizations=authorizations,
          security='Bearer Auth')
db = SQLAlchemy()
mail = Mail() 
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # If use config file inforamation 
    
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app) 
    with app.app_context():

        import apis.users.user
        import apis.slides.slide

        app.register_blueprint(newBlueprint)
        
        CORS(app) 

    # // , resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}}

        return app
