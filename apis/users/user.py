from models.user import User
from api_server import api, bcrypt
from flask_restplus import Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# Define Model
response_base_model = api.model('Base Response Model', {
    'message': fields.String(description='Message'),
    'status_code': fields.Integer(description='Status Code')
})

user_base_model = api.model('User Base Model' , {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'phone': fields.String(required=True, description='Phone')
})

login_model = api.model('Login Model', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

token_model = api.model('Token Model', {
    'access_token': fields.String(description='JWT Access Token'),
    'token_type': fields.String(description='Token Type')
})

user_date_model = api.model('User dates Model', {
    'created_at': fields.String(required=True, description='created_at'),
    'updated_at': fields.String(required=True, description='updated_at')
})

user_response_model = api.inherit('User Response Model', user_base_model, user_date_model, {
    'id': fields.Integer(required=True, description='Id of User'), 
})

user_get_model = api.inherit('User Get Model', response_base_model, {
    'data': fields.List(fields.Nested(user_response_model))
})

#### User API Section #####

# User Signup Route
@api.route('/signup')
@api.doc('create a new user')
class CreateNewUser(Resource):
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
                    identity=user.id,
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
    @jwt_required()
    @api.marshal_with(user_get_model)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    def get(self):
        """Get All Users Functionality"""
        try:
            return User.getAllUsers()
        except Exception as e:
            return {'message': str(e), 'status_code': 400}, 400


            