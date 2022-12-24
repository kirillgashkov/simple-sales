BEGIN;

ALTER TABLE task_types DROP CONSTRAINT IF EXISTS task_types_name_unique;

ALTER TABLE task_priorities DROP CONSTRAINT IF EXISTS task_priorities_name_unique;

ALTER TABLE product_models DROP CONSTRAINT IF EXISTS product_models_name_unique;

ALTER TABLE employee_types DROP CONSTRAINT IF EXISTS employee_types_name_unique;

ALTER TABLE cities DROP CONSTRAINT IF EXISTS cities_city_region_unique;

COMMIT;
