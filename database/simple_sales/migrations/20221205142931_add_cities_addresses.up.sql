BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cities (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_name text NOT NULL,
    region_name text
);
INSERT INTO cities (id, city_name, region_name)
VALUES
    ('16a23ce3-a0f1-49aa-8aa3-34189692aa75', 'Москва', 'Россия'),
    ('6ccf2941-382b-4272-a89a-fe28bf768e49', 'Санкт-Петербург', 'Россия')
ON CONFLICT DO NOTHING;


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
