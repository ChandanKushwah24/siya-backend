from api_server import api, db
from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.slide import Slide, Template, Theme
from werkzeug.datastructures import FileStorage
import base64
import json

# Define Models
theme_model = api.model('Theme Model', {
    'name': fields.String(required=True, description='Theme name'),
    'background_color': fields.String(description='Background color'),
    'text_color': fields.String(description='Text color'),
    'font_family': fields.String(description='Font family')
})

template_model = api.model('Template Model', {
    'name': fields.String(required=True, description='Template name'),
    'layout': fields.Raw(required=True, description='Template layout'),
    'theme_id': fields.Integer(description='Theme ID')
})

slide_model = api.model('Slide Model', {
    'title': fields.String(description='Slide title'),
    'content': fields.Raw(description='Slide content'),
    'template_id': fields.Integer(description='Template ID'),
    'theme_id': fields.Integer(description='Theme ID')
})

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

# Theme APIs
@api.route('/themes')
class ThemeResource(Resource):
    @jwt_required()
    @api.marshal_list_with(theme_model)
    def get(self):
        """Get all themes"""
        return Theme.query.all()

    @jwt_required()
    @api.expect(theme_model)
    def post(self):
        """Create a new theme"""
        data = api.payload
        theme = Theme(**data)
        db.session.add(theme)
        db.session.commit()
        return {'message': 'Theme created successfully', 'id': theme.id}, 201

# Template APIs
@api.route('/templates')
class TemplateResource(Resource):
    @jwt_required()
    @api.marshal_list_with(template_model)
    def get(self):
        """Get all templates"""
        return Template.query.all()

    @jwt_required()
    @api.expect(template_model)
    def post(self):
        """Create a new template"""
        data = api.payload
        template = Template(**data)
        db.session.add(template)
        db.session.commit()
        return {'message': 'Template created successfully', 'id': template.id}, 201

# Slide APIs
@api.route('/slides')
class SlideResource(Resource):
    @jwt_required()
    @api.marshal_list_with(slide_model)
    def get(self):
        """Get all slides for current user"""
        user_id = get_jwt_identity()
        return Slide.query.filter_by(user_id=user_id).all()

    @jwt_required()
    @api.expect(slide_model)
    def post(self):
        """Create a new slide"""
        user_id = get_jwt_identity()
        data = api.payload
        slide = Slide(user_id=user_id, **data)
        db.session.add(slide)
        db.session.commit()
        return {'message': 'Slide created successfully', 'id': slide.id}, 201

@api.route('/slides/<int:id>')
class SlideDetailResource(Resource):
    @jwt_required()
    @api.marshal_with(slide_model)
    def get(self, id):
        """Get a specific slide"""
        user_id = get_jwt_identity()
        slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
        return slide

    @jwt_required()
    @api.expect(slide_model)
    def put(self, id):
        """Update a slide"""
        user_id = get_jwt_identity()
        slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
        data = api.payload
        for key, value in data.items():
            setattr(slide, key, value)
        db.session.commit()
        return {'message': 'Slide updated successfully'}

    @jwt_required()
    def delete(self, id):
        """Delete a slide"""
        user_id = get_jwt_identity()
        slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
        db.session.delete(slide)
        db.session.commit()
        return {'message': 'Slide deleted successfully'}

# Image Upload API
@api.route('/upload-image')
class ImageUploadResource(Resource):
    @jwt_required()
    @api.expect(upload_parser)
    def post(self):
        """Upload an image and return base64 encoded string"""
        args = upload_parser.parse_args()
        image_file = args['file']
        if image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return {'image_data': f'data:image/{image_file.content_type.split("/")[1]};base64,{encoded_image}'}
        return {'message': 'No file uploaded'}, 400