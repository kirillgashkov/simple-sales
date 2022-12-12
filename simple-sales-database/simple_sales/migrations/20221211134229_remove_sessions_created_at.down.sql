BEGIN;

ALTER TABLE sessions ADD COLUMN IF NOT EXISTS created_at timestamp with time zone;
UPDATE sessions SET created_at = expires_at - interval '1 second';
ALTER TABLE sessions ALTER COLUMN created_at SET NOT NULL;
ALTER TABLE sessions ALTER COLUMN created_at SET DEFAULT now();

ALTER TABLE sessions ADD CONSTRAINT expires_at_after_created_at CHECK (expires_at > created_at);

COMMIT;
