-- Adds created_at to the votes table.
-- Safe to run more than once. Existing rows get the time this migration runs.
-- Requires Postgres 11+ (the default is applied without rewriting the table).
ALTER TABLE votes
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now();
