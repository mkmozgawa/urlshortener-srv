from src.api.models import Url


def test_if_url_is_not_in_db_it_shows_no_url_found(test_app, test_database, test_url):
    test_database.session.query(Url).delete()
    client = test_app.test_client()
    r = client.get('/potato', follow_redirects=True)
    assert 'Url not found' in r.data.decode('utf-8')
