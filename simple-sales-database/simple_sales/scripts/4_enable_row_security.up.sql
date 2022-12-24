BEGIN;

ALTER TABLE tasks
ENABLE ROW LEVEL SECURITY,
FORCE ROW LEVEL SECURITY;  -- Apply row level security to table owners as well.

COMMIT;
