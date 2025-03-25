from api_server import api, db, auth_required
from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.image import Image
from models.theme import Theme
from models.slide import Slide

from .templates_data import default_templates
from flask import request
from werkzeug.datastructures import FileStorage
import base64, json, uuid

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
    'theme_id': fields.Integer(description='Theme ID'),
    'preview_image': fields.Nested(api.model('Preview Image', {
        'id': fields.Integer(description='Image ID'),
        'filename': fields.String(description='Image filename'),
        'data': fields.String(description='Base64 encoded image data'),
        'mimetype': fields.String(description='Image MIME type')
    }))
})

slide_model = api.model('Slide Model', {
    'title': fields.String(description='Slide title'),
    'subtitle': fields.String(description='Slide subtitle'),
    'content': fields.String(description='Slide content'),
    'images': fields.List(fields.String, description='List of image URLs'),
    'theme': fields.Nested(api.model('Slide Theme', {
        'backgroundColor': fields.String(description='Background color'),
        'textColor': fields.String(description='Text color'),
        'fontFamily': fields.String(description='Font family'),
        'titleFontSize': fields.String(description='Title font size'),
        'subtitleFontSize': fields.String(description='Subtitle font size'),
        'contentFontSize': fields.String(description='Content font size')
    }))
})

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

# Theme APIs
@api.route('/themes')
class ThemeResource(Resource):
    @auth_required()
    @api.marshal_list_with(theme_model)
    def get(self):
        """Get all themes"""
        try:
            return Theme.query.all()
        except Exception as e:
            return {'message': 'Error fetching themes', 'error': str(e)}, 500

    @auth_required()
    @api.expect(theme_model)
    def post(self):
        """Create a new theme"""
        try:
            data = api.payload
            theme = Theme(**data)
            db.session.add(theme)
            db.session.commit()
            return {'message': 'Theme created successfully', 'id': theme.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error creating theme', 'error': str(e)}, 500

# Template APIs
@api.route('/templates')
class TemplateResource(Resource):
    @auth_required()
    @api.marshal_list_with(template_model)
    def get(self):
        """Get all defult templates"""
        try:
            return default_templates
        except Exception as e:
            return {'message': 'Error fetching templates', 'error': str(e)}, 500

# Slide APIs
@api.route('/slides')
class SlideResource(Resource):
    @auth_required()
    @api.marshal_list_with(slide_model)
    def get(self):
        """Get all slides for current user"""
        try:
            user_id = get_jwt_identity()
            return Slide.query.filter_by(user_id=user_id).all()
        except Exception as e:
            return {'message': 'Error fetching slides', 'error': str(e)}, 500

    @auth_required()
    @api.expect(slide_model)
    def post(self):
        # """Create a new slide"""
        try:
            user_id = get_jwt_identity()
            data = api.payload
            
            # Create or get theme
            theme_data = data.pop('theme', {})

            themeId = str(uuid.uuid4())
            theme = Theme(
                id=themeId,
                background_color=theme_data.get('backgroundColor'),
                text_color=theme_data.get('textColor'),
                font_family=theme_data.get('fontFamily'),
                name=f"Custom Theme {user_id}"
            )
            db.session.add(theme)
            db.session.flush()
            
            # Create slide with theme
            content_data = {
                'title': data.get('title'),
                'subtitle': data.get('subtitle'),
                'content': data.get('content'),
                'images': data.get('images', []),
                'fonts': {
                    'titleFontSize': theme_data.get('titleFontSize'),
                    'subtitleFontSize': theme_data.get('subtitleFontSize'),
                    'contentFontSize': theme_data.get('contentFontSize')
                }
            }
            
            slide = Slide(
                user_id=user_id,
                title=data.get('title'),
                content=content_data,
                theme_id=themeId
            )
            
            db.session.add(slide)
            db.session.commit()
            return {'message': 'Slide created successfully', 'id': slide.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error creating slide', 'error': str(e)}, 500

@api.route('/slides/<int:id>')
class SlideDetailResource(Resource):
    @auth_required()
    @api.marshal_with(slide_model)
    def get(self, id):
        """Get a specific slide"""
        try:
            user_id = get_jwt_identity()
            slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
            return slide
        except Exception as e:
            return {'message': 'Error fetching slide', 'error': str(e)}, 500

    @auth_required()
    @api.expect(slide_model)
    def put(self, id):
        """Update a slide"""
        try:
            user_id = get_jwt_identity()
            slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
            data = api.payload
            for key, value in data.items():
                setattr(slide, key, value)
            db.session.commit()
            return {'message': 'Slide updated successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error updating slide', 'error': str(e)}, 500

    @jwt_required()
    def delete(self, id):
        """Delete a slide"""
        try:
            user_id = get_jwt_identity()
            slide = Slide.query.filter_by(id=id, user_id=user_id).first_or_404()
            db.session.delete(slide)
            db.session.commit()
            return {'message': 'Slide deleted successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error deleting slide', 'error': str(e)}, 500

# Image Upload API
@api.route('/upload-image')
class ImageUploadResource(Resource):
    @auth_required()
    @api.expect(upload_parser)
    def post(self):
        """Upload multiple images and return base64 encoded strings"""
        try:
            user_id = get_jwt_identity()
            args = upload_parser.parse_args()

            image_file = args.get('file')
            if not image_file:
                return {'message': 'No files uploaded'}, 400

            slide_id = request.form.get('slideId')
            if not slide_id:
                return {'message': 'slideId is required'}, 400

            slide = Slide.query.filter_by(id=slide_id, user_id=user_id).first()
            if not slide:
                return {'message': 'Slide not found'}, 404

            uploaded_images = []

            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            # print(image_data)
            image = Image(
                filename=image_file.filename,
                data=image_data,
                mimetype=image_file.content_type,
                size=len(image_data),
                slide_id=slide_id
            )
            db.session.add(image)
            db.session.commit()
            res = f'data:image/{image_file.content_type.split("/")[1]};base64,{encoded_image}'
            return {
                'image_data': res,
                'image_id': image.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'message': 'Error processing image upload', 'error': str(e)}, 500