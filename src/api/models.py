import string
import uuid

import requests as requests
from sqlalchemy.dialects.postgresql import UUID

from src import db


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url = db.Column(db.String(2048))
    custom_name = db.Column(db.String(64), unique=True)

    def __init__(self, target_url):
        if is_responding(target_url):
            self.target_url = target_url
        else:
            raise ValueError

    def create_custom(self, custom_name=None):
        if is_custom_name_valid(custom_name) and not exists_in_db(custom_name):
            self.custom_name = custom_name
        else:
            self.custom_name = get_word()
        return self


def exists_in_db(custom_name):
    return True if Url.query.filter_by(custom_name=custom_name).first() else False


def is_responding(url):
    try:
        r = requests.head(url)
        return r.ok
    except Exception as e:
        return False


def is_custom_name_valid(custom_name):
    """
    Checks that the name:
    * is between 4 and 25 chars
    * contains only ascii chars
    * doesn't contain any whitespace characters
    :param custom_name:
    :return: True if a valid name, False otherwise
    """
    return (
            custom_name
            and 3 < len(custom_name) < 26
            and custom_name.isascii()
            and all(char not in custom_name for char in string.whitespace)
    )


def get_word():
    resp = requests.get('https://random-words-api.vercel.app/word')
    word = resp.json()[0]['word']
    if exists_in_db(word):
        raise KeyError
    return word
