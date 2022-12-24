BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    username text NOT NULL,
    password_hash text NOT NULL,
    employee_id uuid NOT NULL REFERENCES employees (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS users_username_lower_idx ON users (lower(username));


CREATE TABLE IF NOT EXISTS sessions (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL REFERENCES users (id),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    expires_at timestamp with time zone NOT NULL,
    CONSTRAINT expires_at_after_created_at CHECK (expires_at > created_at)
);

COMMIT;
