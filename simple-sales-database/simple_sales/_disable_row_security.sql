BEGIN;

ALTER TABLE tasks
DISABLE ROW LEVEL SECURITY,
NO FORCE ROW LEVEL SECURITY;

COMMIT;
