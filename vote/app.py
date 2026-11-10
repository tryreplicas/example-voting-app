from flask import Flask, render_template, request, make_response, g, jsonify
from redis import Redis
import os
import socket
import random
import json
import logging
import time

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

# Maximum votes accepted per client IP in each fixed window.
VOTE_RATE_LIMIT = 10
VOTE_RATE_WINDOW_SECONDS = 60

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis


def vote_rate_limited(redis, ip):
    # Counters live in Redis so the limit holds across all gunicorn workers.
    window = int(time.time() // VOTE_RATE_WINDOW_SECONDS)
    key = f'ratelimit:vote:{ip}:{window}'
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, VOTE_RATE_WINDOW_SECONDS)
    return count > VOTE_RATE_LIMIT


@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        if vote_rate_limited(redis, request.remote_addr):
            retry_after = VOTE_RATE_WINDOW_SECONDS - int(time.time()) % VOTE_RATE_WINDOW_SECONDS
            resp = make_response('Too many votes, please wait a minute and try again.', 429)
            resp.headers['Retry-After'] = str(retry_after)
            return resp
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


@app.route("/healthz", methods=['GET'])
def healthz():
    return jsonify(status="ok", host=hostname)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
