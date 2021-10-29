import os
import uuid

from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


db = SQLAlchemy(app)


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url = db.Column(db.String(2048))
    custom_name = db.Column(db.String(64), unique=True)


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': 'world!'
        }


api.add_resource(HelloWorld, '/hello')
