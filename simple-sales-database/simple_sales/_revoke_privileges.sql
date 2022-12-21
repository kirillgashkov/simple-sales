BEGIN;

--
-- Role: "simple_sales_salesperson"
--


--
-- Role: "simple_sales_manager"
--


--
-- Role: "simple_sales_admin"
--


-- WARNING: The following commands must be executed from the "simple_sales"
-- database.

REVOKE ALL PRIVILEGES ON ALL ROUTINES IN SCHEMA public FROM simple_sales_admin;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM simple_sales_admin;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM simple_sales_admin;
REVOKE ALL PRIVILEGES ON SCHEMA public FROM simple_sales_admin;

REVOKE ALL PRIVILEGES ON DATABASE simple_sales FROM simple_sales_admin;

COMMIT;
