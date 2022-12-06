BEGIN;

ALTER TABLE contacts DROP COLUMN IF EXISTS address_id;
ALTER TABLE clients DROP COLUMN IF EXISTS organization_address_id;

DROP TABLE IF EXISTS addresses;

COMMIT;
