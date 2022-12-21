REVOKE pam FROM simple_sales_salesperson;

DROP ROLE IF EXISTS pam;

REVOKE jim FROM simple_sales_salesperson;

DROP ROLE IF EXISTS jim;

REVOKE dwight FROM simple_sales_salesperson;

DROP ROLE IF EXISTS dwight;

REVOKE jan FROM simple_sales_manager;

DROP ROLE IF EXISTS jan;

REVOKE michael FROM simple_sales_manager;

DROP ROLE IF EXISTS michael;

REVOKE it_guy FROM simple_sales_admin;

DROP ROLE IF EXISTS it_guy;


DROP ROLE IF EXISTS simple_sales_salesperson;

DROP ROLE IF EXISTS simple_sales_manager;

DROP ROLE IF EXISTS simple_sales_admin;
