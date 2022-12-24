BEGIN;

CREATE FUNCTION is_valid_role_name(role_name name) RETURNS boolean AS $$
    SELECT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = role_name
    );
$$ LANGUAGE SQL;

CREATE TABLE IF NOT EXISTS database_users (
    role_name name PRIMARY KEY,
    employee_id uuid NOT NULL REFERENCES employees (id),
    -- We can't use a foreign key here because role names
    -- are stored in a system table which is not accessible.
    CONSTRAINT valid_role_name CHECK (is_valid_role_name(role_name))
);

CREATE FUNCTION get_current_employee_id() RETURNS uuid AS $$
    SELECT employee_id FROM database_users WHERE role_name = current_user;
$$ LANGUAGE SQL;

COMMIT;
