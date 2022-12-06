BEGIN;

CREATE TABLE IF NOT EXISTS addresses (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    postal_code text NOT NULL,
    city_id uuid NOT NULL REFERENCES cities (id),
    street text NOT NULL,
    house text NOT NULL,
    apartment text,
    note text
);

ALTER TABLE clients ADD COLUMN IF NOT EXISTS organization_address_id uuid REFERENCES addresses (id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS address_id uuid REFERENCES addresses (id);

COMMIT;
