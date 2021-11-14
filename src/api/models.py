import string
import uuid

import requests as requests
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from src import db


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url = db.Column(db.String(2048))
    custom_name = db.Column(db.String(64), unique=True)

    @validates('target_url')
    def validate_target_url(self, key, target_url):
        r = requests.head(target_url)
        return target_url

    @validates('custom_name')
    def validate_custom_name(self, key, custom_name):
        if (
                3 < len(custom_name) < 26
                and custom_name.isascii()
                and all(char not in custom_name for char in string.whitespace)
        ):
            return custom_name
        return Url.get_word()

    def __init__(self, target_url):
        self.target_url = target_url

    def create_custom(self, custom_name=None):
        if Url.exists_in_db(custom_name=custom_name) or custom_name is None:
            self.custom_name = self.get_word()
        else:
            self.custom_name = custom_name
        return self

    @staticmethod
    def find_in_db(**kwargs):
        if 'custom_name' in kwargs.keys():
            return Url.query.filter_by(custom_name=kwargs['custom_name']).first()
        if 'target_url' in kwargs.keys():
            return Url.query.filter_by(target_url=kwargs['target_url']).first()

    @staticmethod
    def exists_in_db(**kwargs):
        return bool(Url.find_in_db(**kwargs))

    @staticmethod
    def get_word():
        resp = requests.get('https://random-words-api.vercel.app/word')
        word = resp.json()[0]['word']
        if Url.exists_in_db(custom_name=word):
            raise KeyError
        return word
