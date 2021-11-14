from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import Url

urls_bp = Blueprint('urls', __name__)
api = Api(urls_bp)


url = api.model('Url', {
    'target_url': fields.String(required=True, description='Url to be redirected to'),
    'custom_name': fields.String(description='Url name to be used as a shortcut')
}, mask="{target_url,custom_name}")


class Urls(Resource):
    @api.doc(responses={200: 'Found', 404: 'Not Found'})
    @api.marshal_with(url)
    def get(self, custom_name):
        if not (target_url := Url.find_in_db(custom_name=custom_name)):
            print(target_url)
            api.abort(404, f'This custom name {custom_name} has no target url, create one with POST')
        return target_url, 200


class UrlsList(Resource):

    @api.expect(url, validate=True)
    @api.doc(responses={201: 'Created', 400: 'Client error'})
    def post(self):
        post_data = request.get_json()
        target_url = post_data.get('target_url')
        custom_name = post_data.get('custom_name')
        try:
            custom_url = Url(target_url).create_custom(custom_name)
        except ValueError:
            return {'message': 'Target url validation failed'}, 400
        except KeyError:
            return {'message': 'Name generation failed, please try again'}, 400
        db.session.add(custom_url)
        db.session.commit()
        return {'target_url': custom_url.target_url, 'custom_name': custom_url.custom_name}, 201


api.add_resource(Urls, '/url/<string:custom_name>')
api.add_resource(UrlsList, '/url')
