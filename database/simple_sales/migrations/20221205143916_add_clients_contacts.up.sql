BEGIN;

CREATE TABLE IF NOT EXISTS clients (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_name text NOT NULL,
    city_id uuid REFERENCES cities (id)
);

CREATE TABLE IF NOT EXISTS contacts (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid NOT NULL REFERENCES clients (id),
    first_name text,
    middle_name text,
    last_name text,
    phone text,
    email text,
    address_id uuid REFERENCES addresses (id),
    note text,
    CONSTRAINT at_least_one_name_or_note CHECK (num_nonnulls(first_name, middle_name, last_name, note) > 0)
);

COMMIT;
