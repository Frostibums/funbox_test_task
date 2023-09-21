import json
import time
import pytest
from django.test import Client
from django.urls import reverse

from links.redis import redis_instance


client = Client()


@pytest.fixture(scope='function')
def test_redis_instance():
    yield
    redis_instance.flushdb()


@pytest.fixture()
def valid_links():
    links = {
        "links": [
            "https://example.com",
            "https://test.com"
        ]
    }
    return links


@pytest.fixture()
def invalid_links():
    links = {
        "links": [
            "invalid_link",
            "http://",
        ]
    }
    return links


# visited_links related tests


def test_visited_links_post(test_redis_instance, valid_links):
    url = reverse('visited_links')
    response = client.post(url, json.dumps(valid_links), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_visited_links_get():
    url = reverse('visited_links')
    response = client.get(url)
    assert response.status_code == 405
    assert response.json() == {"status": "only POST method allowed"}


def test_visited_links_bad_link(test_redis_instance, invalid_links):
    url = reverse('visited_links')
    response = client.post(url, json.dumps(invalid_links), content_type='application/json')
    assert response.status_code == 400
    assert response.json() == {"status": "bad link: invalid_link (doesn't contain a domain)"}


# visited_domains related tests


def test_visited_domains_get(test_redis_instance):
    url = reverse('visited_domains')
    response = client.get(url, {'from': 0, 'to': int(time.time())})
    assert response.status_code == 200
    assert response.json() == {"domains": [], "status": "ok"}


def test_visited_domains_post(test_redis_instance):
    url = reverse('visited_domains')
    response = client.post(url, {'from': 0, 'to': int(time.time())})
    assert response.status_code == 405
    assert response.json() == {"status": "only GET method allowed"}


def test_visited_domains_invalid_params(test_redis_instance):
    url = reverse('visited_domains')
    response = client.get(url, {'from': 'invalid', 'to': 'invalid'})
    assert response.status_code == 400
    assert response.json() == {"status": "'from' must be integer"}

    response = client.get(url, {'from': 0, 'to': 'invalid'})
    assert response.status_code == 400
    assert response.json() == {"status": "'to' must be integer"}
