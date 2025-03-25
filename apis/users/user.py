from models.user import User
from api_server import api, bcrypt, auth_required
from flask_restplus import Resource, fields
from flask_jwt_extended import create_access_token
from datetime import timedelta

# API Response and Request Models

# Base response model for consistent API responses
response_base_model = api.model('Base Response Model', {
    'message': fields.String(description='Response message indicating success/failure'),
    'status_code': fields.Integer(description='HTTP status code of the response')
})

# Model for user registration and basic user data
user_base_model = api.model('User Base Model' , {
    'username': fields.String(required=True, description='Unique username for the user account'),
    'email': fields.String(required=True, description='Valid email address for the account'),
    'password': fields.String(required=True, description='Strong password meeting security requirements'),
})

# Model for user authentication
login_model = api.model('Login Model', {
    'email': fields.String(required=True, description='Registered email address'),
    'password': fields.String(required=True, description='Account password')
})

# Model for JWT token response
token_model = api.model('Token Model', {
    'access_token': fields.String(description='JWT token for API authentication'),
    'token_type': fields.String(description='Token type (e.g., "Bearer")')
})

# Model for user timestamps
user_date_model = api.model('User dates Model', {
    'created_at': fields.String(required=True, description='Account creation timestamp'),
    'updated_at': fields.String(required=True, description='Last update timestamp')
})

# Extended user model including all user information
user_response_model = api.inherit('User Response Model', user_base_model, user_date_model, {
    'id': fields.Integer(required=True, description='Unique user identifier'), 
})

# Model for user listing endpoint response
user_get_model = api.inherit('User Get Model', response_base_model, {
    'data': fields.List(fields.Nested(user_response_model), description='List of user objects')
})

#### User Authentication API Endpoints ####

@api.route('/signup')
@api.doc('User Registration Endpoint')
class CreateNewUser(Resource):
    """Handles new user registration.
    
    This endpoint validates user input, ensures username and email uniqueness,
    and creates a new user account with a securely hashed password.
    """
    @api.expect(user_base_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid request')
    def post(self):
        """Creates a new User"""
        try:
            User.createUser(api.payload)
            return {'message': 'User created successfully','status_code': 201}, 201
        except Exception as e:
            return {'message': str(e), 'status_code': 400}, 400

# User Login Route
@api.route('/login')
@api.doc('user login')
class UserLogin(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """User login and token generation"""
        try:
            data = api.payload
            user = User.query.filter_by(email=data['email']).first()
            
            if user and bcrypt.check_password_hash(user.password, data['password']):
                access_token = create_access_token(
                    identity=str(user.id),
                    expires_delta=timedelta(days=1)
                )
                return {
                    'access_token': access_token,
                    'token_type': 'bearer'
                }, 200
            
            return {'message': 'Invalid credentials', 'status_code': 401}, 401
        except Exception as e:
            return {'message': str(e), 'status_code': 400}, 400

# Get All Users
@api.route('/users') 
class GetAllUsers(Resource):
    @auth_required()
    @api.marshal_with(user_get_model)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    def get(self):
        """Get All Users Functionality"""
        try:
            return User.getAllUsers()
        except Exception as e:
            return {'message': str(e), 'status_code': 400}, 400


            