BEGIN;

--
-- Role: "simple_sales_salesperson"
--


--
-- Role: "simple_sales_manager"
--


REVOKE DELETE
ON tasks
FROM simple_sales_manager;


REVOKE UPDATE (
    -- id,
    task_type_id,
    task_priority_id,
    note,
    contact_id,
    contract_number,
    product_serial_number,
    -- created_at,
    due_at,
    completed_at,
    created_by,
    assigned_to
)
ON tasks
FROM simple_sales_manager;


REVOKE INSERT (
    -- id,
    task_type_id,
    task_priority_id,
    note,
    contact_id,
    contract_number,
    product_serial_number,
    -- created_at,
    due_at,
    -- completed_at,
    created_by,
    assigned_to
)
ON tasks
FROM simple_sales_manager;


--
-- Role: "simple_sales_employee" (includes "simple_sales_manager" and "simple_sales_salesperson")
--


REVOKE UPDATE (completed_at)
ON tasks
FROM simple_sales_employee;


REVOKE
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
FROM
    simple_sales_employee;


REVOKE CONNECT ON DATABASE simple_sales FROM simple_sales_employee;


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
