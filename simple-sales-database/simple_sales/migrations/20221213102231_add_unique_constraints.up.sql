BEGIN;

ALTER TABLE cities DROP CONSTRAINT IF EXISTS cities_city_region_unique;
ALTER TABLE cities ADD CONSTRAINT cities_city_region_unique UNIQUE NULLS NOT DISTINCT (city, region);

ALTER TABLE employee_types DROP CONSTRAINT IF EXISTS employee_types_name_unique;
ALTER TABLE employee_types ADD CONSTRAINT employee_types_name_unique UNIQUE (name);

ALTER TABLE product_models DROP CONSTRAINT IF EXISTS product_models_name_unique;
ALTER TABLE product_models ADD CONSTRAINT product_models_name_unique UNIQUE (name);

ALTER TABLE task_priorities DROP CONSTRAINT IF EXISTS task_priorities_name_unique;
ALTER TABLE task_priorities ADD CONSTRAINT task_priorities_name_unique UNIQUE (name);

ALTER TABLE task_types DROP CONSTRAINT IF EXISTS task_types_name_unique;
ALTER TABLE task_types ADD CONSTRAINT task_types_name_unique UNIQUE (name);

COMMIT;
