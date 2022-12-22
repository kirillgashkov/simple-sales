BEGIN;

--
-- Role: "simple_sales_admin"
--


-- Grant "all" privileges on the database to the "simple_sales_admin" role.
-- (Some new objects (e.g. schema) may require additional privileges to be
-- granted.)
--
-- See:
--
-- * https://www.postgresql.org/docs/current/sql-grant.html,
-- * https://www.postgresql.org/docs/current/ddl-priv.html,
-- * https://stackoverflow.com/q/22483555.

GRANT ALL PRIVILEGES ON DATABASE simple_sales TO simple_sales_admin;

-- WARNING: The following commands must be executed from the "simple_sales"
-- database.

GRANT ALL PRIVILEGES ON SCHEMA public TO simple_sales_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO simple_sales_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO simple_sales_admin;
GRANT ALL PRIVILEGES ON ALL ROUTINES IN SCHEMA public TO simple_sales_admin;


--
-- Role: "simple_sales_employee" (includes "simple_sales_manager" and "simple_sales_salesperson")
--


GRANT CONNECT ON DATABASE simple_sales TO simple_sales_employee;

GRANT
    SELECT
ON
    addresses,
    cities,
    clients,
    contacts,
    contracts,
    contracts_products,
    employee_types,
    employees,
    product_models,
    products,
    -- schema_migrations,
    -- sessions,
    task_priorities,
    task_types,
    tasks
    -- users
TO
    simple_sales_employee;


--
-- Role: "simple_sales_manager"
--


--
-- Role: "simple_sales_salesperson"
--

COMMIT;
