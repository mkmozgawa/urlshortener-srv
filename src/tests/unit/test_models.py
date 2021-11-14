import pytest
import requests.exceptions

from src.api.models import Url


def test_urls_with_invalid_custom_names_cannot_be_created(test_app, test_database):
    url = Url('https://google.com')
    assert url.create_custom(3 * 'a').custom_name != 3 * 'a'
    assert url.create_custom(26 * 'a').custom_name != 26 * 'a'
    assert url.create_custom('goog le').custom_name != 'goog le'
    assert url.create_custom('goog\nle').custom_name != 'goog\nle'
    assert url.create_custom('goog\rle').custom_name != 'goog\rle'
    assert url.create_custom('goog\vle').custom_name != 'goog\vle'
    assert url.create_custom('').custom_name != ''
    assert url.create_custom(None).custom_name is not None


def test_urls_with_invalid_target_urls_cannot_be_created(test_app, test_database):
    with pytest.raises(ValueError):
        Url('')
    with pytest.raises(ValueError):
        Url('https://thisdomainprobablyshouldntexistpotatosalad.com')
    with pytest.raises(ValueError):
        Url('https://gool le.com')
    with pytest.raises(ValueError):
        Url('')
    with pytest.raises(ValueError):
        Url(None)


def test_urls_without_schema_should_have_it_added(test_app, test_database):
    assert Url('google.com').target_url == 'https://google.com'
    assert Url('https://google.com').target_url == 'https://google.com'
    assert Url('http://google.com').target_url == 'http://google.com'
