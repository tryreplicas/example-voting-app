-- Creates the votes table the worker writes to and the result app reads from.
-- Safe to run more than once: every statement checks whether it is needed first.

CREATE TABLE IF NOT EXISTS votes (
    id VARCHAR(255) NOT NULL UNIQUE,
    vote VARCHAR(255) NOT NULL
);

-- The result app counts votes with GROUP BY vote, so index that column.
CREATE INDEX IF NOT EXISTS votes_vote_idx ON votes (vote);
