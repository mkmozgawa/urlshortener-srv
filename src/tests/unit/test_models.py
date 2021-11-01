from src.api.models import is_custom_name_valid, is_responding


def test_is_responding_rejects_invalid_urls():
    assert not is_responding('google.com')
    assert not is_responding('https://thisdomainprobablyshouldntexistpotatosalad.com')
    assert not is_responding('')


def test_is_custom_name_valid_rejects_invalid_names():
    assert not is_custom_name_valid(3*'a')
    assert not is_custom_name_valid(26*'a')
    assert not is_custom_name_valid('goog le')
    assert not is_custom_name_valid('goog\nle')
    assert not is_custom_name_valid('goog\rle')
    assert not is_custom_name_valid('goog\vle')
    assert not is_custom_name_valid('')
    assert not is_custom_name_valid(None)
