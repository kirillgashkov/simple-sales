BEGIN;

DROP TABLE IF EXISTS sessions;


DROP INDEX IF EXISTS users_username_lower_idx;

DROP TABLE IF EXISTS users;

COMMIT;
