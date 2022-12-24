BEGIN;

ALTER TABLE sessions DROP CONSTRAINT IF EXISTS expires_at_after_created_at;
ALTER TABLE sessions DROP COLUMN IF EXISTS created_at;

COMMIT;
