import json


def test_create_without_providing_custom_name(test_app, test_database, test_url):
    client = test_app.test_client()
    status_code, data = test_url(client, target_url='https://google.com')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']
    assert type(data['custom_name']) == str


def test_the_same_generated_custom_name_is_not_returned(test_app, test_database, test_url):
    client = test_app.test_client()
    _, data_1 = test_url(client, target_url='https://google.com')
    _, data_2 = test_url(client, target_url='https://google.com')
    assert data_1['custom_name'] != data_2['custom_name']


def test_create_with_providing_custom_name(test_app, test_database, test_url):
    client = test_app.test_client()
    status_code, data = test_url(client, target_url='https://google.com', custom_name='potato')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name'] == 'potato'


def test_returns_error_if_no_target_provided(test_app, test_database, test_url):
    client = test_app.test_client()
    status_code, data = test_url(client, custom_name='potato')
    assert status_code == 400
    assert data['errors']['target_url'] == '\'target_url\' is a required property'


def test_returns_error_if_target_is_not_correctly_passed(test_app, test_database, test_url):
    client = test_app.test_client()
    status_code, data = test_url(client, target_url='google.com')
    assert status_code == 400
    assert data['message'] == '\'target_url\' is incorrect, did you forget to add https://?'


def test_generates_another_custom_name_if_custom_name_is_taken(test_app, test_database, test_url):
    client = test_app.test_client()
    test_url(client, target_url='https://google.com', custom_name='potato')
    status_code, data = test_url(client, target_url='https://google.com', custom_name='potato')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']


def test_generates_a_custom_name_for_provided_invalid_custom_names(test_app, test_database, test_url):
    client = test_app.test_client()
    status_code, data = test_url(client, target_url='https://google.com', custom_name='aa')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']
