BEGIN;

CREATE TABLE IF NOT EXISTS employee_types (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name text NOT NULL
);

INSERT INTO employee_types (id, name)
VALUES
    ('4cf1d446-8624-4176-9121-18c3b0cca623', 'manager'),
    ('fb6b4665-556b-4a12-b7f0-333f73ca6f16', 'salesperson')
ON CONFLICT DO NOTHING;


CREATE TABLE IF NOT EXISTS employees (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_type_id uuid NOT NULL REFERENCES employee_types (id),
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL,
    city_id uuid NOT NULL REFERENCES cities(id)
);

COMMIT;
