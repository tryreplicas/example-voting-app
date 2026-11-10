import pytest

import app as app_module
from app import app


class FakeRedis:
    def __init__(self):
        self.counts = {}
        self.expires = {}
        self.votes = []

    def incr(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]

    def expire(self, key, seconds):
        self.expires[key] = seconds

    def rpush(self, key, value):
        self.votes.append((key, value))


@pytest.fixture
def redis(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(app_module, 'get_redis', lambda: fake)
    return fake


@pytest.fixture
def clock(monkeypatch):
    now = [1_000_000.0]
    monkeypatch.setattr(app_module.time, 'time', lambda: now[0])
    return now


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def vote(client, choice='a', ip='10.0.0.1'):
    return client.post('/', data={'vote': choice}, environ_base={'REMOTE_ADDR': ip})


def test_votes_up_to_limit_are_accepted(client, redis):
    for _ in range(app_module.VOTE_RATE_LIMIT):
        assert vote(client).status_code == 200

    assert len(redis.votes) == app_module.VOTE_RATE_LIMIT


def test_vote_over_limit_is_rejected_and_not_recorded(client, redis):
    for _ in range(app_module.VOTE_RATE_LIMIT):
        vote(client)

    resp = vote(client)

    assert resp.status_code == 429
    assert 'Retry-After' in resp.headers
    assert len(redis.votes) == app_module.VOTE_RATE_LIMIT


def test_limit_is_per_ip(client, redis):
    for _ in range(app_module.VOTE_RATE_LIMIT):
        vote(client, ip='10.0.0.1')

    assert vote(client, ip='10.0.0.1').status_code == 429
    assert vote(client, ip='10.0.0.2').status_code == 200


def test_limit_resets_after_window(client, redis, clock):
    for _ in range(app_module.VOTE_RATE_LIMIT):
        vote(client)
    assert vote(client).status_code == 429

    clock[0] += app_module.VOTE_RATE_WINDOW_SECONDS

    assert vote(client).status_code == 200


def test_counter_expires_with_window(client, redis):
    vote(client)

    assert list(redis.expires.values()) == [app_module.VOTE_RATE_WINDOW_SECONDS]


def test_get_requests_do_not_count_against_limit(client, redis):
    for _ in range(app_module.VOTE_RATE_LIMIT + 5):
        assert client.get('/').status_code == 200

    assert redis.counts == {}
    assert vote(client).status_code == 200
