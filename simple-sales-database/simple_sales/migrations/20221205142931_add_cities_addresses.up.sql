BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cities (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_name text NOT NULL,
    region_name text
);

CREATE TABLE IF NOT EXISTS addresses (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    postal_code text NOT NULL,
    city_id uuid NOT NULL REFERENCES cities (id),
    street text NOT NULL,
    house text NOT NULL,
    apartment text,
    note text
);

COMMIT;
