from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import Url, exists_in_db

urls_bp = Blueprint('urls', __name__)
api = Api(urls_bp)

url = api.model('Url', {
    'id': fields.String(readOnly=True),
    'target_url': fields.String(required=True, description='Url to be redirected to'),
    'custom_name': fields.String(description='Url name to be used as a shortcut')
})


class Urls(Resource):
    @api.expect(url, validate=True)
    def post(self):
        post_data = request.get_json()
        target_url = post_data.get('target_url')
        custom_name = post_data.get('custom_name')
        try:
            custom_url = Url(target_url).create_custom(custom_name)
        except ValueError:
            return {'message': '\'target_url\' is incorrect, did you forget to add https://?'}, 400
        except KeyError:
            return {'message': 'Name generation failed, please try again'}
        db.session.add(custom_url)
        db.session.commit()
        return {'target_url': custom_url.target_url, 'custom_name': custom_url.custom_name}, 201


api.add_resource(Urls, '/url')
