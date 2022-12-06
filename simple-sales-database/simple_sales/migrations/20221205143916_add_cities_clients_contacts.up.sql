BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cities (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_name text NOT NULL,
    region_name text
);

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
    note text,
    CONSTRAINT at_least_one_name_or_note CHECK (num_nonnulls(first_name, middle_name, last_name, note) > 0)
);

COMMIT;
