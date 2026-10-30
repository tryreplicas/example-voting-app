import socket

import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_healthz_returns_ok(client):
    resp = client.get('/healthz')

    assert resp.status_code == 200
    assert resp.mimetype == 'application/json'
    assert resp.get_json()['status'] == 'ok'


def test_healthz_includes_host(client):
    resp = client.get('/healthz')

    assert resp.get_json()['host'] == socket.gethostname()


def test_healthz_rejects_post(client):
    resp = client.post('/healthz')

    assert resp.status_code == 405
