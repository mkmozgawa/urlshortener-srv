import json


def test_create_without_providing_custom_name(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/url',
        data=json.dumps({
            'target_url': 'https://google.com'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']
    assert type(data['custom_name']) == str


def test_create_with_providing_custom_name(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/url',
        data=json.dumps({
            'target_url': 'https://google.com',
            'custom_name': 'potato'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name'] == 'potato'


def test_returns_error_if_no_target_provided(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/url',
        data=json.dumps({
            'custom_name': 'potato'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['errors']['target_url'] == '\'target_url\' is a required property'


def test_returns_error_if_target_is_not_responding(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/url',
        data=json.dumps({
            'target_url': 'google.com'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['message'] == '\'target_url\' is incorrect, did you forget to add https://?'


def test_returns_error_if_custom_name_is_taken(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/url',
        data=json.dumps({
            'target_url': 'https://google.com',
            'custom_name': 'potato'
        }),
        content_type='application/json'
    )
    resp = client.post(
        '/url',
        data=json.dumps({
            'target_url': 'https://google.com',
            'custom_name': 'potato'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert data['message'] == 'Custom name taken, try another'
