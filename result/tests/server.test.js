const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { test } = require('node:test');
const vm = require('node:vm');

// Exercise the real server's polling lifecycle without a live database or port.
function startServer() {
  const queries = [], timers = [], scores = [], errors = [], handlers = {};
  const pool = {
    query(sql, parameters, callback) { queries.push({ sql, callback }); },
    on(event, callback) { handlers[event] = callback; }
  };
  const app = { use() {}, get() {} };
  const modules = {
    express: Object.assign(() => app, { urlencoded() {}, static() {} }),
    pg: { Pool: function() { return pool; } },
    'cookie-parser': () => {},
    http: { Server: () => ({ listen() {} }) },
    'socket.io': () => ({
      on() {},
      sockets: { emit(event, payload) { scores.push({ event, payload }); } }
    })
  };
  vm.runInNewContext(readFileSync(require.resolve('../server.js'), 'utf8'), {
    require(name) {
      assert.ok(name in modules, `Unexpected dependency: ${name}`);
      return modules[name];
    },
    process: { env: {} },
    __dirname: require('node:path').resolve(__dirname, '..'),
    console: { log() {}, error(message) { errors.push(message); } },
    setTimeout(callback, delay) { timers.push({ callback, delay }); }
  });
  return {
    queries, timers, scores, errors, handlers,
    nextPoll() {
      const timer = timers.shift();
      assert.equal(timer.delay, 1000);
      timer.callback();
    }
  };
}

function finishQuery(server, rows) {
  const query = server.queries.shift();
  assert.equal(query.sql, 'SELECT vote, COUNT(id) AS count FROM votes GROUP BY vote');
  query.callback(null, { rows });
}

test('broadcasts updated totals, changed votes, and empty results', () => {
  const server = startServer();
  assert.equal(server.queries.length, 1);
  assert.equal(server.timers.length, 0, 'queries must not overlap');
  finishQuery(server, [{ vote: 'a', count: '2' }, { vote: 'b', count: '1' }]);
  server.nextPoll();
  finishQuery(server, [{ vote: 'b', count: '3' }]);
  server.nextPoll();
  finishQuery(server, []);
  assert.deepEqual(server.scores.map(score => [score.event, JSON.parse(score.payload)]), [
    ['scores', { a: 2, b: 1 }], ['scores', { a: 0, b: 3 }], ['scores', { a: 0, b: 0 }]
  ]);
});

test('retries query failures and publishes fresh counts after recovery', () => {
  const server = startServer();
  finishQuery(server, [{ vote: 'a', count: '1' }]);
  server.nextPoll();
  server.queries.shift().callback(new Error('Connection terminated unexpectedly'));
  assert.equal(server.scores.length, 1, 'do not publish fabricated counts during an outage');
  assert.match(server.errors[0], /Connection terminated/);
  server.nextPoll();
  finishQuery(server, [{ vote: 'a', count: '2' }]);
  assert.deepEqual(JSON.parse(server.scores[1].payload), { a: 2, b: 0 });
});

test('recovers from database unavailability at startup', () => {
  const server = startServer();
  server.queries.shift().callback(new Error('connect ECONNREFUSED'));
  assert.equal(server.scores.length, 0);
  server.nextPoll();
  finishQuery(server, [{ vote: 'b', count: '1' }]);
  assert.deepEqual(JSON.parse(server.scores[0].payload), { a: 0, b: 1 });
});

test('handles idle connection errors and continues polling', () => {
  const server = startServer();
  finishQuery(server, []);
  server.handlers.error(new Error('terminating connection due to administrator command'));
  assert.match(server.errors[0], /administrator command/);
  server.nextPoll();
  finishQuery(server, [{ vote: 'b', count: '2' }]);
  assert.deepEqual(JSON.parse(server.scores[1].payload), { a: 0, b: 2 });
});
