\connect simple_sales


DROP OWNED BY simple_sales_admin CASCADE;
DROP OWNED BY simple_sales_manager CASCADE;
DROP OWNED BY simple_sales_salesperson CASCADE;
DROP OWNED BY simple_sales_employee CASCADE;


\connect postgres


-- Admin
DROP ROLE IF EXISTS simple_sales_admin;

-- Manager
REVOKE simple_sales_employee FROM simple_sales_manager;
DROP ROLE IF EXISTS simple_sales_manager;

-- Salesperson
REVOKE simple_sales_employee FROM simple_sales_salesperson;
DROP ROLE IF EXISTS simple_sales_salesperson;

-- Employee
DROP ROLE IF EXISTS simple_sales_employee;


DROP DATABASE simple_sales;
