CREATE DATABASE simple_sales;

REVOKE CONNECT ON DATABASE simple_sales FROM PUBLIC;


-- Employee
CREATE ROLE simple_sales_employee
WITH
    NOINHERIT;

-- Salesperson
CREATE ROLE simple_sales_salesperson
WITH
    INHERIT;

GRANT simple_sales_employee TO simple_sales_salesperson;

-- Manager
CREATE ROLE simple_sales_manager
WITH
    INHERIT;

GRANT simple_sales_employee TO simple_sales_manager;

-- Admin
CREATE ROLE simple_sales_admin
WITH
    NOINHERIT
    CREATEDB
    CREATEROLE;
