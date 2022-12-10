BEGIN;

ALTER TABLE cities RENAME COLUMN region TO region_name;

ALTER TABLE cities RENAME COLUMN city TO city_name;

COMMIT;
