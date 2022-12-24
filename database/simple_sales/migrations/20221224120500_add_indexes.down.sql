BEGIN;

DROP INDEX IF EXISTS contacts_email_idx;
DROP INDEX IF EXISTS contacts_phone_idx;
DROP INDEX IF EXISTS contacts_last_name_idx;
DROP INDEX IF EXISTS contacts_middle_name_idx;
DROP INDEX IF EXISTS contacts_first_name_idx;
DROP INDEX IF EXISTS clients_organization_name_idx;
DROP INDEX IF EXISTS cities_region_idx;
DROP INDEX IF EXISTS cities_name_idx;

COMMIT;
