BEGIN;

ALTER TABLE cities RENAME COLUMN city_name TO city;

ALTER TABLE cities RENAME COLUMN region_name TO region;

COMMIT;
