BEGIN;

CREATE INDEX IF NOT EXISTS cities_name_idx ON cities (name);
CREATE INDEX IF NOT EXISTS cities_region_idx ON cities (region);
CREATE INDEX IF NOT EXISTS clients_organization_name_idx ON clients (organization_name);
CREATE INDEX IF NOT EXISTS contacts_first_name_idx ON contacts (first_name);
CREATE INDEX IF NOT EXISTS contacts_middle_name_idx ON contacts (middle_name);
CREATE INDEX IF NOT EXISTS contacts_last_name_idx ON contacts (last_name);
CREATE INDEX IF NOT EXISTS contacts_phone_idx ON contacts (phone);
CREATE INDEX IF NOT EXISTS contacts_email_idx ON contacts (email);

COMMIT;
