import pytest

from links.services import get_domain_from_url


@pytest.fixture
def test_valid_urls():
    urls = [
        'https://testurl.com',
        'testurl.com',
        'https://testurl.com?aabs=1233&bs=fa',
        'www.testurl.com',
    ]
    return urls


@pytest.fixture
def test_invalid_urls():
    urls = [
        'https://testurl',
        'testurl',
        '?aabs=1233&bs=fa',
        'www..com',
    ]
    return urls


def test_get_domain_from_url_valid_url(test_valid_urls):
    for url in test_valid_urls:
        assert get_domain_from_url(url) == 'testurl.com'


def test_get_domain_from_url_invalid_url(test_invalid_urls):
    for url in test_invalid_urls:
        assert get_domain_from_url(url) == False
