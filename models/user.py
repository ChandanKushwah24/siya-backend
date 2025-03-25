from api_server import db
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'db_key'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # hass password
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def validate_email(email):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if bool(email_pattern.match(email)):
            return True, ''
        return False, "Invalid email format"

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        return True, ''

    @staticmethod
    def validate_phone(phone):
        phone_pattern = re.compile(r'^\+91[1-9][0-9]{9}$')
        if not bool(phone_pattern.match(phone)):
            return False, "Invalid phone number format. Please use Indian international format (e.g., +911234567890)"
        return True, ''

    @staticmethod
    def validate_username(username):
        if len(username) < 3 or len(username) > 50:
            return False, "Username must be between 3 and 50 characters"
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        return True, ''

    @staticmethod
    def validate_fields(data):
        required_fields = ['username', 'email', 'password', 'phone']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate each field and collect errors
        validation_errors = []
        
        # Username validation
        is_valid, error = User.validate_username(data['username'])
        if not is_valid:
            validation_errors.append(error)
        
        # Email validation
        is_valid, error = User.validate_email(data['email'])
        if not is_valid:
            validation_errors.append(error)
        
        # Password validation
        is_valid, error = User.validate_password(data['password'])
        if not is_valid:
            validation_errors.append(error)
        
        # Phone validation
        is_valid, error = User.validate_phone(data['phone'])
        if not is_valid:
            validation_errors.append(error)

        # If there are any validation errors, raise them
        if validation_errors:
            raise ValueError("\n".join(validation_errors))

        try:
            # Check for existing username
            if User.query.filter_by(username=data['username']).first():
                raise ValueError("Username already exists")
            
            # Check for existing email
            if User.query.filter_by(email=data['email']).first():
                raise ValueError("Email already exists")
        except Exception as e:
            if 'duplicate key value violates unique constraint' in str(e):
                if 'users_username_key' in str(e):
                    raise ValueError("Username already exists")
                if 'users_email_key' in str(e):
                    raise ValueError("Email already exists")
            raise
        
        return True

    @staticmethod
    def createUser(data):
        """Create a new user with validation and password hashing"""
        try:
            # Validate all fields
            User.validate_fields(data)
            
            # Hash the password
            from api_server import bcrypt
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            # Create new user instance
            new_user = User(
                username=data['username'],
                email=data['email'],
                password=hashed_password,
                phone=data['phone']
            )
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            # Return user data without sensitive information
            return {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'phone': new_user.phone,
                'created_at': new_user.created_at,
                'updated_at': new_user.updated_at
            }
        except ValueError as ve:
            db.session.rollback()
            raise ve
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating user: {str(e)}")
