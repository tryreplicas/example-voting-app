-- Add a created_at timestamp to the votes table.
--
-- The worker creates the votes table on startup, so run this after the worker
-- has connected at least once. Safe to run more than once.
--
-- Existing rows get the time this migration runs, since their real vote time
-- was never recorded. New votes get the insert time from the default.

BEGIN;

ALTER TABLE votes
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now();

COMMIT;
