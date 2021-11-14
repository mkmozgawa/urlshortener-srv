import pytest

from src.api.models import Url


# url shortening tests
def test_create_without_providing_custom_name(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='https://google.com')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']
    assert type(data['custom_name']) == str


def test_the_same_generated_custom_name_is_not_returned(test_app, test_database, test_create_url):
    client = test_app.test_client()
    _, data_1 = test_create_url(client, target_url='https://google.com')
    _, data_2 = test_create_url(client, target_url='https://google.com')
    assert data_1['custom_name'] != data_2['custom_name']


def test_create_with_providing_custom_name(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='https://google.com', custom_name='potato')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name'] == 'potato'


def test_returns_error_if_no_target_provided(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, custom_name='potato')
    assert status_code == 400
    assert data['errors']['target_url'] == '\'target_url\' is a required property'


def test_adds_prefix_if_target_has_no_protocol_provided(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='google.com')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']


def test_returns_error_for_incorrect_target_url(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='https://goog le.com')
    assert status_code == 400
    assert 'Target url validation failed' in data['message']


def test_returns_error_for_not_responding_target_url(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='https://thisdomainprobablyshouldntexistpotatosalad.com')
    assert status_code == 400
    assert 'Target url validation failed' in data['message']


def test_returns_error_for_empty_target_url(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='')
    assert status_code == 400
    assert 'Target url validation failed' in data['message']


def test_generates_another_custom_name_if_custom_name_is_taken(test_app, test_database, test_create_url):
    client = test_app.test_client()
    test_create_url(client, target_url='https://google.com', custom_name='potato')
    status_code, data = test_create_url(client, target_url='https://google.com', custom_name='potato')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']


def test_generates_a_custom_name_for_provided_invalid_custom_names(test_app, test_database, test_create_url):
    client = test_app.test_client()
    status_code, data = test_create_url(client, target_url='https://google.com', custom_name='aa')
    assert status_code == 201
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name']


# url lookup tests
def test_if_custom_name_exists_in_db_its_target_url_is_returned(test_app, test_database, test_create_url,
                                                                test_lookup_url):
    client = test_app.test_client()
    _, data = test_create_url(client, target_url='https://google.com', custom_name='potato')
    status_code, data = test_lookup_url(client, 'potato')
    assert status_code == 200
    assert data['target_url'] == 'https://google.com'
    assert data['custom_name'] == 'potato'


def test_if_custom_name_doesnt_exist_in_db_error_message_is_returned(test_app, test_database, test_lookup_url):
    test_database.session.query(Url).delete()
    client = test_app.test_client()
    status_code, data = test_lookup_url(client, 'potato')
    assert status_code == 404
    'This custom name has no target url, create one with POST' in data['message']


def test_only_target_url_is_returned_if_its_mask_is_applied(test_app, test_database, test_create_url, test_lookup_url):
    client = test_app.test_client()
    _, data = test_create_url(client, target_url='https://google.com', custom_name='potato')
    status_code, data = test_lookup_url(client, 'potato', {'X-Fields': 'target_url'})
    assert status_code == 200
    assert data['target_url'] == 'https://google.com'
    with pytest.raises(KeyError):
        data['custom_name']
