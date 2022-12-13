BEGIN;

ALTER TABLE cities RENAME COLUMN city TO name;

ALTER TABLE cities RENAME CONSTRAINT cities_city_region_unique TO cities_name_region_unique;

COMMIT;
