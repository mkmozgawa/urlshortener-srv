from flask_restx import Resource, Api
from flask import Blueprint

hello_bp = Blueprint('hello', __name__)
api = Api(hello_bp)


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': 'world!'
        }


api.add_resource(HelloWorld, '/hello')
