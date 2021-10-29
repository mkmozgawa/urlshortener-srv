from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import Url

urls_bp = Blueprint('urls', __name__)
api = Api(urls_bp)

url = api.model('Url', {
    'id': fields.String(readOnly=True),
    'target_url': fields.String(required=True),
    'custom_name': fields.String
})


class Urls(Resource):
    @api.expect(url, validate=True)
    def post(self):
        post_data = request.get_json()
        target_url = post_data.get('target_url')
        custom_name = post_data.get('custom_name')
        if Url.query.filter_by(custom_name=custom_name).first():
            return {'message': 'Custom name taken, try another'}, 400
        url = Url(target_url).create_custom(custom_name)
        db.session.add(url)
        db.session.commit()
        return {'target_url': url.target_url, 'custom_name': url.custom_name}, 201


api.add_resource(Urls, '/url')
