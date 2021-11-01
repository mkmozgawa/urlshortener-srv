import json

import pytest

from src import db, create_app


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def test_url():
    def _test_url(client, **kwargs):
        resp = client.post(
            '/url',
            data=json.dumps(kwargs),
            content_type='application/json'
        )
        return resp.status_code, json.loads(resp.data.decode())
    return _test_url
