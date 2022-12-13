BEGIN;

ALTER TABLE cities RENAME CONSTRAINT cities_name_region_unique TO cities_city_region_unique;

ALTER TABLE cities RENAME COLUMN name TO city;

COMMIT;
