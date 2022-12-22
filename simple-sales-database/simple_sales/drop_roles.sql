-- Temporary roles for development.

REVOKE simple_sales_salesperson FROM pam;
DROP ROLE IF EXISTS pam;

REVOKE simple_sales_salesperson FROM jim;
DROP ROLE IF EXISTS jim;

REVOKE simple_sales_salesperson FROM dwight;
DROP ROLE IF EXISTS dwight;

REVOKE simple_sales_manager FROM jan;
DROP ROLE IF EXISTS jan;

REVOKE simple_sales_manager FROM michael;
DROP ROLE IF EXISTS michael;

REVOKE simple_sales_admin FROM it_guy;
DROP ROLE IF EXISTS it_guy;


REVOKE simple_sales_employee FROM simple_sales_salesperson;
DROP ROLE IF EXISTS simple_sales_salesperson;

REVOKE simple_sales_employee FROM simple_sales_manager;
DROP ROLE IF EXISTS simple_sales_manager;

DROP ROLE IF EXISTS simple_sales_employee;

DROP ROLE IF EXISTS simple_sales_admin;
